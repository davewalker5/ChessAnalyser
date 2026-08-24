"""Tk desktop interface for the PGN editor."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

import chess

from pgn_editor.game import GameModel, MoveRejectedError
from pgn_editor.persistence import PgnFileError, load_pgn, save_pgn

APP_BACKGROUND = "#07111f"
SURFACE = "#0d1b2d"
SURFACE_RAISED = "#13243a"
FIELD_BACKGROUND = "#081524"
BORDER = "#213750"
TEXT = "#eff6ff"
MUTED_TEXT = "#8fa6be"
ACCENT = "#35d4d0"
LIGHT_SQUARE = "#c5dcda"
DARK_SQUARE = "#426d73"
SELECTED_SQUARE = "#d8b84c"
TARGET_SQUARE = "#8fba69"
BLACK_PIECE = "#151515"
WHITE_PIECE = "#f7f7f7"
WHITE_PIECE_OUTLINE = "#303030"
BOARD_MARGIN = 28
MINIMUM_BOARD_SIZE = 320
PIECE_GLYPHS = {
    chess.PAWN: "♟",
    chess.KNIGHT: "♞",
    chess.BISHOP: "♝",
    chess.ROOK: "♜",
    chess.QUEEN: "♛",
    chess.KING: "♚",
}


class PgnEditor(tk.Tk):
    """Main PGN editor application window."""

    def __init__(self) -> None:
        """Create and lay out a PGN editor window."""
        super().__init__()
        self.model = GameModel()
        self.current_path: Path | None = None
        self.dirty = False
        self.white_at_bottom = True
        self.drag_source: chess.Square | None = None
        self.drag_target: chess.Square | None = None
        self.board_pixels = MINIMUM_BOARD_SIZE
        self.title("PGN Editor")
        self.minsize(760, 500)
        # The two-panel layout is naturally wide. A taller default window makes
        # the square board width-constrained and creates large empty bands above
        # and below both panels.
        self.geometry("1000x580")
        self.configure(background=APP_BACKGROUND)
        self._configure_styles()
        self._create_menu()
        self._create_widgets()
        self._bind_shortcuts()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._refresh()

    def _configure_styles(self) -> None:
        """Apply a dark, cyan-accented visual theme to native widgets."""
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=APP_BACKGROUND)
        style.configure(
            "Panel.TFrame",
            background=SURFACE,
            bordercolor=BORDER,
            relief=tk.SOLID,
            borderwidth=1,
        )
        style.configure(
            "TLabel",
            background=APP_BACKGROUND,
            foreground=TEXT,
            font=("TkDefaultFont", 12),
        )
        style.configure(
            "Eyebrow.TLabel",
            background=SURFACE,
            foreground=ACCENT,
            font=("TkDefaultFont", 10, "bold"),
        )
        style.configure(
            "Heading.TLabel",
            background=SURFACE,
            foreground=TEXT,
            font=("TkDefaultFont", 20, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background=SURFACE_RAISED,
            foreground=MUTED_TEXT,
            padding=(12, 9),
            font=("TkDefaultFont", 10),
        )
        style.configure(
            "TButton",
            background=SURFACE_RAISED,
            foreground=ACCENT,
            bordercolor="#397b82",
            lightcolor=SURFACE_RAISED,
            darkcolor=SURFACE_RAISED,
            padding=(14, 9),
            font=("TkDefaultFont", 10, "bold"),
        )
        style.map(
            "TButton",
            background=[("active", "#18384a"), ("pressed", "#1d4654")],
            foreground=[("active", TEXT), ("disabled", "#536a80")],
            bordercolor=[("active", ACCENT), ("focus", ACCENT)],
        )
        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground=APP_BACKGROUND,
            bordercolor=ACCENT,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#64e1dd"), ("pressed", "#28b9b6")],
            foreground=[("active", APP_BACKGROUND)],
        )
        style.configure(
            "Vertical.TScrollbar",
            background=SURFACE_RAISED,
            troughcolor=FIELD_BACKGROUND,
            bordercolor=BORDER,
            arrowcolor=MUTED_TEXT,
        )

    def _create_menu(self) -> None:
        """Create conventional file and edit menus."""
        menu_options = {
            "background": SURFACE,
            "foreground": TEXT,
            "activebackground": SURFACE_RAISED,
            "activeforeground": ACCENT,
            "borderwidth": 0,
        }
        menu = tk.Menu(self, **menu_options)
        file_menu = tk.Menu(menu, tearoff=False, **menu_options)
        file_menu.add_command(label="Open…", accelerator="Ctrl+O", command=self._open)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self._save)
        file_menu.add_command(
            label="Save As…", accelerator="Ctrl+Shift+S", command=self._save_as
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        menu.add_cascade(label="File", menu=file_menu)
        edit_menu = tk.Menu(menu, tearoff=False, **menu_options)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self._undo)
        edit_menu.add_command(label="Clear Game", command=self._clear)
        edit_menu.add_command(label="Flip Board", command=self._flip)
        menu.add_cascade(label="Edit", menu=edit_menu)
        self.config(menu=menu)

    def _create_widgets(self) -> None:
        """Create the two-panel editor layout and controls."""
        container = ttk.Frame(self, padding=(18, 7))
        container.pack(fill=tk.BOTH, expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2, minsize=260)
        container.rowconfigure(0, weight=1)

        board_frame = ttk.Frame(container)
        board_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        self.canvas = tk.Canvas(
            board_frame, highlightthickness=0, background=APP_BACKGROUND
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self._draw_board)
        self.canvas.bind("<ButtonPress-1>", self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self._drag_end)

        self.panel = ttk.Frame(container, style="Panel.TFrame", padding=20)
        self.panel.grid(row=0, column=1, sticky="ew")
        self.panel.grid_propagate(False)
        self.panel.rowconfigure(1, weight=1)
        self.panel.columnconfigure(0, weight=1)
        heading = ttk.Frame(self.panel, style="Panel.TFrame")
        heading.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        ttk.Label(heading, text="CURRENT GAME", style="Eyebrow.TLabel").pack(anchor="w")
        ttk.Label(heading, text="Move notation", style="Heading.TLabel").pack(
            anchor="w", pady=(3, 0)
        )
        move_frame = ttk.Frame(self.panel, style="Panel.TFrame")
        move_frame.grid(row=1, column=0, sticky="nsew")
        move_frame.rowconfigure(0, weight=1)
        move_frame.columnconfigure(0, weight=1)
        self.move_text = tk.Text(
            move_frame,
            state=tk.DISABLED,
            wrap=tk.NONE,
            width=30,
            padx=14,
            pady=14,
            cursor="arrow",
            background=FIELD_BACKGROUND,
            foreground=TEXT,
            selectbackground=ACCENT,
            selectforeground=APP_BACKGROUND,
            insertbackground=ACCENT,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            highlightthickness=1,
            borderwidth=0,
            font=("TkFixedFont", 12),
        )
        scrollbar = ttk.Scrollbar(
            move_frame, orient=tk.VERTICAL, command=self.move_text.yview
        )
        self.move_text.configure(yscrollcommand=scrollbar.set)
        self.move_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        controls = ttk.Frame(self.panel, style="Panel.TFrame")
        controls.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.undo_button = ttk.Button(controls, text="Undo", command=self._undo)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 5))
        self.clear_button = ttk.Button(controls, text="Clear", command=self._clear)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Flip", command=self._flip).pack(side=tk.LEFT, padx=5)
        self.status = ttk.Label(
            self.panel, text="Ready", anchor="w", style="Status.TLabel"
        )
        self.status.grid(row=3, column=0, sticky="ew", pady=(10, 0))

    def _bind_shortcuts(self) -> None:
        """Bind common platform-neutral keyboard shortcuts."""
        self.bind_all("<Control-o>", lambda event: self._open())
        self.bind_all("<Control-s>", lambda event: self._save())
        self.bind_all("<Control-Shift-S>", lambda event: self._save_as())
        self.bind_all("<Control-z>", lambda event: self._undo())

    def _draw_board(self, event: tk.Event[tk.Misc] | None = None) -> None:
        """Draw a square, labelled board fitted to the available canvas."""
        del event
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        self.board_pixels = max(min(width, height) - 2 * BOARD_MARGIN, 8)
        self.board_x = (width - self.board_pixels) / 2
        self.board_y = (height - self.board_pixels) / 2
        if hasattr(self, "panel"):
            labelled_board_height = min(height, self.board_pixels + 2 * BOARD_MARGIN)
            self.panel.configure(height=int(labelled_board_height))
        square_size = self.board_pixels / 8
        files = "ABCDEFGH" if self.white_at_bottom else "HGFEDCBA"
        ranks = "87654321" if self.white_at_bottom else "12345678"
        for display_rank in range(8):
            for display_file in range(8):
                x0 = self.board_x + display_file * square_size
                y0 = self.board_y + display_rank * square_size
                square = self._display_to_square(display_file, display_rank)
                colour = (
                    LIGHT_SQUARE
                    if (display_file + display_rank) % 2 == 0
                    else DARK_SQUARE
                )
                if square == self.drag_source:
                    colour = SELECTED_SQUARE
                elif square == self.drag_target:
                    colour = TARGET_SQUARE
                self.canvas.create_rectangle(
                    x0,
                    y0,
                    x0 + square_size,
                    y0 + square_size,
                    fill=colour,
                    outline=colour,
                )
                piece = self.model.board.piece_at(square)
                if piece is not None:
                    glyph = PIECE_GLYPHS[piece.piece_type]
                    centre_x = x0 + square_size / 2
                    centre_y = y0 + square_size / 2
                    piece_font = ("Arial", max(20, int(square_size * 0.94)))
                    if piece.color == chess.WHITE:
                        # The offset copy gives light pieces a visible edge on both
                        # board colours without relying on platform-specific emoji.
                        self.canvas.create_text(
                            centre_x + max(1, square_size * 0.025),
                            centre_y + max(1, square_size * 0.025),
                            text=glyph,
                            fill=WHITE_PIECE_OUTLINE,
                            font=piece_font,
                        )
                    self.canvas.create_text(
                        centre_x,
                        centre_y,
                        text=glyph,
                        fill=WHITE_PIECE if piece.color == chess.WHITE else BLACK_PIECE,
                        font=piece_font,
                    )
        coordinate_font = ("TkDefaultFont", max(8, int(square_size * 0.16)), "bold")
        for index in range(8):
            centre_x = self.board_x + (index + 0.5) * square_size
            centre_y = self.board_y + (index + 0.5) * square_size
            self.canvas.create_text(
                centre_x,
                self.board_y - 12,
                text=files[index],
                fill=MUTED_TEXT,
                font=coordinate_font,
            )
            self.canvas.create_text(
                centre_x,
                self.board_y + self.board_pixels + 12,
                text=files[index],
                fill=MUTED_TEXT,
                font=coordinate_font,
            )
            self.canvas.create_text(
                self.board_x - 13,
                centre_y,
                text=ranks[index],
                fill=MUTED_TEXT,
                font=coordinate_font,
            )
            self.canvas.create_text(
                self.board_x + self.board_pixels + 13,
                centre_y,
                text=ranks[index],
                fill=MUTED_TEXT,
                font=coordinate_font,
            )

    def _display_to_square(self, display_file: int, display_rank: int) -> chess.Square:
        """Convert a displayed row and column to a python-chess square."""
        if self.white_at_bottom:
            return chess.square(display_file, 7 - display_rank)
        return chess.square(7 - display_file, display_rank)

    def _square_at(self, x: int, y: int) -> chess.Square | None:
        """Return the board square at canvas coordinates, if any."""
        size = self.board_pixels / 8
        display_file = int((x - self.board_x) // size)
        display_rank = int((y - self.board_y) // size)
        if not 0 <= display_file < 8 or not 0 <= display_rank < 8:
            return None
        return self._display_to_square(display_file, display_rank)

    def _drag_start(self, event: tk.Event[tk.Misc]) -> None:
        """Begin dragging when the pointer is over a piece."""
        square = self._square_at(event.x, event.y)
        if square is not None and self.model.board.piece_at(square) is not None:
            self.drag_source = square
            self.drag_target = None
            self._draw_board()

    def _drag_motion(self, event: tk.Event[tk.Misc]) -> None:
        """Highlight the destination square currently beneath the pointer."""
        if self.drag_source is None:
            return
        target = self._square_at(event.x, event.y)
        if target == self.drag_source:
            target = None
        if target != self.drag_target:
            self.drag_target = target
            self._draw_board()

    def _drag_end(self, event: tk.Event[tk.Misc]) -> None:
        """Attempt to complete a dragged move."""
        source = self.drag_source
        destination = self._square_at(event.x, event.y)
        self.drag_source = None
        self.drag_target = None
        if source is None or destination is None or source == destination:
            self._draw_board()
            return
        promotion = self._promotion_for(source, destination)
        if promotion is False:
            self._draw_board()
            return
        try:
            san = self.model.add_move(source, destination, promotion)
        except MoveRejectedError as error:
            self.status.configure(text=str(error))
            self.bell()
        else:
            self.dirty = True
            self.status.configure(text=f"Added {san}")
        self._refresh()

    def _promotion_for(
        self, source: chess.Square, destination: chess.Square
    ) -> chess.PieceType | None | bool:
        """Prompt for a promotion piece when a pawn reaches the final rank."""
        piece = self.model.board.piece_at(source)
        if piece is None or piece.piece_type != chess.PAWN:
            return None
        if chess.square_rank(destination) not in (0, 7):
            return None
        choice = show_dialog(
            self,
            "Promote pawn",
            "Choose the piece for this promotion.",
            (
                ("Queen", "queen"),
                ("Rook", "rook"),
                ("Bishop", "bishop"),
                ("Knight", "knight"),
            ),
            default="queen",
        )
        promotion_types = {
            "queen": chess.QUEEN,
            "rook": chess.ROOK,
            "bishop": chess.BISHOP,
            "knight": chess.KNIGHT,
        }
        return promotion_types.get(choice, False)

    def _refresh(self) -> None:
        """Synchronise board, move text, controls, and window title."""
        self._draw_board()
        san = self.model.san_moves()
        lines = []
        for index in range(0, len(san), 2):
            black = san[index + 1] if index + 1 < len(san) else ""
            lines.append(f"{index // 2 + 1:>3}.  {san[index]:<12} {black}")
        self.move_text.configure(state=tk.NORMAL)
        self.move_text.delete("1.0", tk.END)
        self.move_text.insert("1.0", "\n".join(lines))
        self.move_text.configure(state=tk.DISABLED)
        self.move_text.see(tk.END)
        state = tk.NORMAL if self.model.has_moves else tk.DISABLED
        self.undo_button.configure(state=state)
        self.clear_button.configure(state=state)
        name = self.current_path.name if self.current_path else "Untitled.pgn"
        marker = " *" if self.dirty else ""
        self.title(f"{name}{marker} — PGN Editor")

    def _undo(self) -> None:
        """Undo the final recorded move."""
        if self.model.undo():
            self.dirty = True
            self.status.configure(text="Last move removed")
            self._refresh()

    def _clear(self) -> None:
        """Confirm and clear the current game's moves."""
        if not self.model.has_moves:
            return
        answer = show_dialog(
            self,
            "Clear game",
            "Remove all moves from this game?",
            (("Clear game", "clear"), ("Cancel", "cancel")),
            default="cancel",
        )
        if answer != "clear":
            return
        self.model.clear()
        self.dirty = True
        self.status.configure(text="Game cleared")
        self._refresh()

    def _flip(self) -> None:
        """Reverse board orientation without changing game state."""
        self.white_at_bottom = not self.white_at_bottom
        self._draw_board()

    def _open(self) -> None:
        """Prompt for and transactionally load a PGN file."""
        if not self._may_discard_changes():
            return
        filename = filedialog.askopenfilename(
            parent=self,
            title="Open PGN",
            filetypes=(("PGN files", "*.pgn"), ("All files", "*.*")),
        )
        if not filename:
            return
        path = Path(filename)
        try:
            loaded = load_pgn(path)
        except PgnFileError as error:
            show_dialog(
                self,
                "Could not open PGN",
                str(error),
                (("Close", "close"),),
            )
            return
        self.model = loaded.model
        self.current_path = path
        self.dirty = False
        self.status.configure(text=f"Opened {path.name}")
        self._refresh()
        if loaded.additional_games:
            show_dialog(
                self,
                "Additional games",
                "Only the first game was loaded.",
                (("Continue", "continue"),),
            )

    def _save(self) -> bool:
        """Save to the current path, prompting for one if necessary."""
        if self.current_path is None:
            return self._save_as()
        return self._write(self.current_path)

    def _save_as(self) -> bool:
        """Prompt for a destination and save the current game."""
        filename = filedialog.asksaveasfilename(
            parent=self,
            title="Save PGN",
            defaultextension=".pgn",
            filetypes=(("PGN files", "*.pgn"), ("All files", "*.*")),
            confirmoverwrite=True,
            initialfile=self.current_path.name if self.current_path else "game.pgn",
        )
        if not filename:
            return False
        return self._write(Path(filename))

    def _write(self, path: Path) -> bool:
        """Write the game and update file state only after success."""
        try:
            save_pgn(path, self.model)
        except PgnFileError as error:
            show_dialog(
                self,
                "Could not save PGN",
                str(error),
                (("Close", "close"),),
            )
            return False
        self.current_path = path
        self.dirty = False
        self.status.configure(text=f"Saved {path.name}")
        self._refresh()
        return True

    def _may_discard_changes(self) -> bool:
        """Ask whether unsaved work should be saved, discarded, or retained."""
        if not self.dirty:
            return True
        answer = show_dialog(
            self,
            "Unsaved changes",
            "Save changes before continuing?",
            (("Save", "save"), ("Discard", "discard"), ("Cancel", "cancel")),
            default="save",
        )
        if answer in (None, "cancel"):
            return False
        if answer == "save":
            return self._save()
        return True

    def _on_close(self) -> None:
        """Close the application after resolving unsaved changes."""
        if self._may_discard_changes():
            self.destroy()


class StyledDialog(tk.Toplevel):
    """Application-themed modal notification or choice dialog."""

    def __init__(
        self,
        parent: PgnEditor,
        title: str,
        message: str,
        buttons: tuple[tuple[str, str], ...],
        default: str | None,
    ) -> None:
        """Create a modal dialog and its labelled result buttons."""
        super().__init__(parent)
        self.result: str | None = None
        self.withdraw()
        self.title(title)
        self.configure(background=APP_BACKGROUND)
        self.resizable(False, False)
        card = ttk.Frame(self, style="Panel.TFrame", padding=24)
        card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        ttk.Label(card, text="PGN EDITOR", style="Eyebrow.TLabel").pack(anchor="w")
        ttk.Label(card, text=title, style="Heading.TLabel").pack(
            anchor="w", pady=(5, 12)
        )
        ttk.Label(
            card,
            text=message,
            style="Eyebrow.TLabel",
            foreground=MUTED_TEXT,
            font=("TkDefaultFont", 12),
            wraplength=390,
            justify=tk.LEFT,
        ).pack(anchor="w", pady=(0, 22))
        button_bar = ttk.Frame(card, style="Panel.TFrame")
        button_bar.pack(fill=tk.X)
        default_button: ttk.Button | None = None
        for index, (label, value) in enumerate(buttons):
            button = ttk.Button(
                button_bar,
                text=label,
                style="Accent.TButton" if value == default else "TButton",
                command=lambda selected=value: self._choose(selected),
            )
            button.pack(
                side=tk.LEFT, expand=True, fill=tk.X, padx=(0 if index == 0 else 6, 0)
            )
            if value == default:
                default_button = button
        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.bind("<Escape>", lambda event: self._cancel())
        if default_button is not None:
            self.bind("<Return>", lambda event: default_button.invoke())
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_reqwidth()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_reqheight()) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")
        self.deiconify()
        self.grab_set()
        (default_button or button).focus_set()

    def _choose(self, result: str) -> None:
        """Store a selected result and close the dialog."""
        self.result = result
        self.destroy()

    def _cancel(self) -> None:
        """Close the dialog without selecting a result."""
        self.destroy()


def show_dialog(
    parent: PgnEditor,
    title: str,
    message: str,
    buttons: tuple[tuple[str, str], ...],
    default: str | None = None,
) -> str | None:
    """Display an application-themed modal dialog and return its result."""
    dialog = StyledDialog(parent, title, message, buttons, default)
    parent.wait_window(dialog)
    return dialog.result


def main() -> None:
    """Start the PGN editor desktop application."""
    PgnEditor().mainloop()
