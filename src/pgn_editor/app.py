"""Tk desktop interface for the PGN editor."""

import tkinter as tk
from calendar import Calendar
from datetime import UTC, date, datetime
from pathlib import Path
from tkinter import filedialog, ttk

import chess

from pgn_editor.game import (
    PGN_METADATA_DEFAULTS,
    FutureMovesError,
    GameModel,
    MoveRejectedError,
)
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
ILLEGAL_TARGET_SQUARE = "#a84b5d"
LEGAL_MOVE_MARKER = "#35d4d0"
BLACK_PIECE = "#151515"
WHITE_PIECE = "#f7f7f7"
WHITE_PIECE_OUTLINE = "#303030"
BOARD_MARGIN = 28
MINIMUM_BOARD_SIZE = 320
DEFAULT_PLAYBACK_SECONDS = 1.0
MINIMUM_PLAYBACK_SECONDS = 0.25
MAXIMUM_PLAYBACK_SECONDS = 5.0
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
        self.legal_drag_targets: frozenset[chess.Square] = frozenset()
        self.playback_after_id: str | None = None
        self.playback_seconds = tk.DoubleVar(value=DEFAULT_PLAYBACK_SECONDS)
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
            "Section.TLabel",
            background=SURFACE,
            foreground=TEXT,
            font=("TkDefaultFont", 14, "bold"),
        )
        style.configure(
            "Metadata.TLabel",
            background=SURFACE,
            foreground=MUTED_TEXT,
            font=("TkDefaultFont", 9, "bold"),
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
            "Transport.TButton",
            background=SURFACE_RAISED,
            foreground=ACCENT,
            bordercolor="#397b82",
            lightcolor=SURFACE_RAISED,
            darkcolor=SURFACE_RAISED,
            padding=(3, 7),
            font=("TkDefaultFont", 14, "bold"),
        )
        style.map(
            "Transport.TButton",
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
            "Calendar.TButton",
            background=SURFACE_RAISED,
            foreground=ACCENT,
            bordercolor=BORDER,
            lightcolor=SURFACE_RAISED,
            darkcolor=SURFACE_RAISED,
            padding=(5, 4),
            font=("TkDefaultFont", 10, "bold"),
        )
        style.map(
            "Calendar.TButton",
            background=[("active", "#18384a"), ("pressed", "#1d4654")],
            foreground=[("active", TEXT)],
            bordercolor=[("active", ACCENT), ("focus", ACCENT)],
        )
        style.configure(
            "Vertical.TScrollbar",
            background=SURFACE_RAISED,
            troughcolor=FIELD_BACKGROUND,
            bordercolor=BORDER,
            arrowcolor=MUTED_TEXT,
        )
        style.configure(
            "Horizontal.TScale",
            background=SURFACE,
            troughcolor=FIELD_BACKGROUND,
            bordercolor=BORDER,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
        )
        style.configure(
            "TEntry",
            fieldbackground=FIELD_BACKGROUND,
            foreground=TEXT,
            insertcolor=ACCENT,
            bordercolor=BORDER,
            lightcolor=FIELD_BACKGROUND,
            darkcolor=FIELD_BACKGROUND,
            padding=(7, 5),
        )
        style.map("TEntry", bordercolor=[("focus", ACCENT)])
        style.configure(
            "TCombobox",
            fieldbackground=FIELD_BACKGROUND,
            background=SURFACE_RAISED,
            foreground=TEXT,
            arrowcolor=ACCENT,
            bordercolor=BORDER,
            lightcolor=FIELD_BACKGROUND,
            darkcolor=FIELD_BACKGROUND,
            padding=(7, 5),
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", FIELD_BACKGROUND)],
            foreground=[("readonly", TEXT)],
            bordercolor=[("focus", ACCENT)],
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
        self.panel.rowconfigure(2, weight=1)
        self.panel.columnconfigure(0, weight=1)

        metadata_panel = ttk.Frame(self.panel, style="Panel.TFrame")
        metadata_panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        metadata_panel.columnconfigure(0, weight=1)
        metadata_panel.columnconfigure(1, weight=1)
        ttk.Label(metadata_panel, text="GAME DETAILS", style="Eyebrow.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 5)
        )

        self.calendar_icon = self._create_calendar_icon()
        self.metadata_variables: dict[str, tk.StringVar] = {}
        field_names = tuple(PGN_METADATA_DEFAULTS)
        for index, name in enumerate(field_names):
            row = index // 2 + 1
            column = index % 2
            field = ttk.Frame(metadata_panel, style="Panel.TFrame")
            field.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=(0, 8) if column == 0 else (8, 0),
                pady=2,
            )
            field.columnconfigure(1, weight=1)
            ttk.Label(field, text=name.upper(), style="Metadata.TLabel").grid(
                row=0, column=0, sticky="w", padx=(0, 6)
            )
            variable = tk.StringVar(value=self.model.headers[name])
            self.metadata_variables[name] = variable
            if name == "Result":
                editor: ttk.Entry | ttk.Combobox = ttk.Combobox(
                    field,
                    textvariable=variable,
                    values=("*", "1-0", "0-1", "1/2-1/2"),
                    state="readonly",
                    width=12,
                )
                editor.bind(
                    "<<ComboboxSelected>>",
                    lambda event, field_name=name: self._commit_metadata_field(
                        field_name
                    ),
                )
            else:
                editor = ttk.Entry(field, textvariable=variable, width=12)
                editor.bind(
                    "<Return>",
                    lambda event, field_name=name: self._commit_metadata_field(
                        field_name
                    ),
                )
                if name == "Date":
                    ttk.Button(
                        field,
                        image=self.calendar_icon,
                        style="Calendar.TButton",
                        command=self._pick_date,
                    ).grid(row=0, column=2, sticky="e", padx=(4, 0))
            editor.bind(
                "<FocusOut>",
                lambda event, field_name=name: self._commit_metadata_field(field_name),
            )
            editor.grid(row=0, column=1, sticky="ew")

        ttk.Label(self.panel, text="Move notation", style="Section.TLabel").grid(
            row=1, column=0, sticky="w", pady=(0, 6)
        )
        move_frame = ttk.Frame(self.panel, style="Panel.TFrame")
        move_frame.grid(row=2, column=0, sticky="nsew")
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

        navigation = ttk.Frame(self.panel, style="Panel.TFrame")
        navigation.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        self.start_button = ttk.Button(
            navigation,
            text="⏮",
            width=2,
            style="Transport.TButton",
            command=self._navigate_start,
        )
        self.back_button = ttk.Button(
            navigation,
            text="◀◀",
            width=2,
            style="Transport.TButton",
            command=self._navigate_back,
        )
        self.forward_button = ttk.Button(
            navigation,
            text="▶▶",
            width=2,
            style="Transport.TButton",
            command=self._navigate_forward,
        )
        self.end_button = ttk.Button(
            navigation,
            text="⏭",
            width=2,
            style="Transport.TButton",
            command=self._navigate_end,
        )
        self.play_button = ttk.Button(
            navigation,
            text="▶",
            width=2,
            style="Transport.TButton",
            command=self._play,
        )
        self.pause_button = ttk.Button(
            navigation,
            text="⏸",
            width=2,
            style="Transport.TButton",
            command=self._pause,
        )
        for index, button in enumerate(
            (
                self.start_button,
                self.back_button,
                self.forward_button,
                self.end_button,
                self.play_button,
                self.pause_button,
            )
        ):
            button.pack(
                side=tk.LEFT,
                expand=True,
                fill=tk.X,
                padx=(0 if index == 0 else 3, 0),
            )

        speed_controls = ttk.Frame(self.panel, style="Panel.TFrame")
        speed_controls.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        self.speed_label = ttk.Label(
            speed_controls,
            text="Playback: 1.00 seconds",
            style="Eyebrow.TLabel",
        )
        self.speed_label.pack(anchor="w")
        ttk.Scale(
            speed_controls,
            from_=MINIMUM_PLAYBACK_SECONDS,
            to=MAXIMUM_PLAYBACK_SECONDS,
            variable=self.playback_seconds,
            command=self._playback_speed_changed,
        ).pack(fill=tk.X, pady=(5, 0))

        controls = ttk.Frame(self.panel, style="Panel.TFrame")
        controls.grid(row=5, column=0, sticky="ew", pady=(8, 0))
        self.undo_button = ttk.Button(controls, text="Undo", command=self._undo)
        self.undo_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 3))
        self.clear_button = ttk.Button(controls, text="Clear", command=self._clear)
        self.clear_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
        ttk.Button(controls, text="Flip", command=self._flip).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(3, 0)
        )
        self.status = ttk.Label(
            self.panel, text="Ready", anchor="w", style="Status.TLabel"
        )
        self.status.grid(row=6, column=0, sticky="ew", pady=(8, 0))

    def _bind_shortcuts(self) -> None:
        """Bind common platform-neutral keyboard shortcuts."""
        self.bind_all("<Control-o>", lambda event: self._open())
        self.bind_all("<Control-s>", lambda event: self._save())
        self.bind_all("<Control-Shift-S>", lambda event: self._save_as())
        self.bind_all("<Control-z>", lambda event: self._undo())

    def _create_calendar_icon(self) -> tk.PhotoImage:
        """Create a crisp themed calendar icon without a platform font glyph."""
        icon = tk.PhotoImage(width=24, height=24)
        icon.put(ACCENT, to=(2, 4, 22, 22))
        icon.put(FIELD_BACKGROUND, to=(4, 9, 20, 20))
        icon.put(TEXT, to=(6, 1, 8, 7))
        icon.put(TEXT, to=(16, 1, 18, 7))
        icon.put(MUTED_TEXT, to=(6, 12, 9, 14))
        icon.put(MUTED_TEXT, to=(11, 12, 14, 14))
        icon.put(MUTED_TEXT, to=(16, 12, 19, 14))
        icon.put(MUTED_TEXT, to=(6, 16, 9, 18))
        icon.put(MUTED_TEXT, to=(11, 16, 14, 18))
        icon.put(MUTED_TEXT, to=(16, 16, 19, 18))
        return icon

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
                    colour = (
                        TARGET_SQUARE
                        if square in self.legal_drag_targets
                        else ILLEGAL_TARGET_SQUARE
                    )
                self.canvas.create_rectangle(
                    x0,
                    y0,
                    x0 + square_size,
                    y0 + square_size,
                    fill=colour,
                    outline=colour,
                )
                piece = self.model.board.piece_at(square)
                if (
                    square in self.legal_drag_targets
                    and square != self.drag_target
                    and piece is None
                ):
                    marker_radius = square_size * 0.09
                    centre_x = x0 + square_size / 2
                    centre_y = y0 + square_size / 2
                    self.canvas.create_oval(
                        centre_x - marker_radius,
                        centre_y - marker_radius,
                        centre_x + marker_radius,
                        centre_y + marker_radius,
                        fill=LEGAL_MOVE_MARKER,
                        outline="",
                    )
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
                    if square in self.legal_drag_targets and square != self.drag_target:
                        capture_inset = square_size * 0.08
                        self.canvas.create_oval(
                            x0 + capture_inset,
                            y0 + capture_inset,
                            x0 + square_size - capture_inset,
                            y0 + square_size - capture_inset,
                            outline=LEGAL_MOVE_MARKER,
                            width=max(2, int(square_size * 0.04)),
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
            self._stop_playback()
            legal_targets = self.model.legal_destinations(square)
            if not legal_targets:
                message = self.model.game_over_message
                self.status.configure(text=message or "That piece has no legal moves.")
                self.bell()
                return
            self.drag_source = square
            self.drag_target = None
            self.legal_drag_targets = legal_targets
            self.status.configure(text="Choose a highlighted destination")
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
        legal_targets = self.legal_drag_targets
        self.drag_source = None
        self.drag_target = None
        self.legal_drag_targets = frozenset()
        if source is None or destination is None or source == destination:
            self._draw_board()
            return
        if destination not in legal_targets:
            self.status.configure(text="Illegal move")
            self.bell()
            self._refresh()
            return
        promotion = self._promotion_for(source, destination)
        if promotion is False:
            self._draw_board()
            return
        try:
            san = self.model.add_move(source, destination, promotion)
        except FutureMovesError:
            answer = show_dialog(
                self,
                "Replace later moves?",
                "Editing from this position will discard all later moves.",
                (("Replace", "replace"), ("Cancel", "cancel")),
                default="cancel",
            )
            if answer != "replace":
                self._refresh()
                return
            try:
                san = self.model.add_move(
                    source, destination, promotion, replace_future=True
                )
            except MoveRejectedError as error:
                self.status.configure(text=str(error))
                self.bell()
                self._refresh()
                return
        except MoveRejectedError as error:
            self.status.configure(text=str(error))
            self.bell()
        else:
            self.dirty = True
            self.status.configure(text=self.model.game_over_message or f"Added {san}")
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
        self._render_moves()
        previous_state = tk.NORMAL if self.model.has_previous_position else tk.DISABLED
        next_state = tk.NORMAL if self.model.has_next_position else tk.DISABLED
        self.start_button.configure(state=previous_state)
        self.back_button.configure(state=previous_state)
        self.forward_button.configure(state=next_state)
        self.end_button.configure(state=next_state)
        self.play_button.configure(
            state=(
                tk.NORMAL
                if self.model.has_next_position and self.playback_after_id is None
                else tk.DISABLED
            )
        )
        self.pause_button.configure(
            state=tk.NORMAL if self.playback_after_id is not None else tk.DISABLED
        )
        state = tk.NORMAL if self.model.has_moves else tk.DISABLED
        self.undo_button.configure(state=state)
        self.clear_button.configure(state=state)
        name = self.current_path.name if self.current_path else "Untitled.pgn"
        marker = " *" if self.dirty else ""
        self.title(f"{name}{marker} — PGN Editor")

    def _commit_metadata_field(self, name: str) -> None:
        """Store one edited metadata field and update document state."""
        variable = self.metadata_variables[name]
        try:
            changed = self.model.set_header(name, variable.get())
        except ValueError as error:
            variable.set(self.model.headers[name])
            show_dialog(
                self,
                "Invalid game detail",
                str(error),
                (("Close", "close"),),
            )
            return
        stored_value = self.model.headers[name]
        if variable.get() != stored_value:
            variable.set(stored_value)
        if changed:
            self.dirty = True
            self.status.configure(text=f"Updated {name}")
            self._refresh()

    def _commit_all_metadata(self) -> None:
        """Store any metadata field still being edited."""
        for name in PGN_METADATA_DEFAULTS:
            self._commit_metadata_field(name)

    def _load_metadata_fields(self) -> None:
        """Populate metadata editors from the current game model."""
        headers = self.model.headers
        for name, variable in self.metadata_variables.items():
            variable.set(headers[name])

    def _pick_date(self) -> None:
        """Open a calendar and store a selected date in PGN format."""
        current_text = self.metadata_variables["Date"].get()
        try:
            initial_date = date.fromisoformat(current_text.replace(".", "-"))
        except ValueError:
            initial_date = datetime.now(UTC).astimezone().date()
        dialog = CalendarDialog(self, initial_date)
        self.wait_window(dialog)
        if dialog.result is not None:
            self.metadata_variables["Date"].set(dialog.result.strftime("%Y.%m.%d"))
            self._commit_metadata_field("Date")

    def _render_moves(self) -> None:
        """Render all SAN moves and highlight the displayed position's move."""
        san = self.model.san_moves()
        self.move_text.configure(state=tk.NORMAL)
        self.move_text.delete("1.0", tk.END)
        for index in range(0, len(san), 2):
            self.move_text.insert(tk.END, f"{index // 2 + 1:>3}.  ")
            white_tag = f"move_{index + 1}"
            self.move_text.insert(tk.END, f"{san[index]:<12}", white_tag)
            self.move_text.tag_configure(
                white_tag, background=FIELD_BACKGROUND, foreground=TEXT
            )
            if index + 1 < len(san):
                black_tag = f"move_{index + 2}"
                self.move_text.insert(tk.END, san[index + 1], black_tag)
                self.move_text.tag_configure(
                    black_tag, background=FIELD_BACKGROUND, foreground=TEXT
                )
            if index + 2 < len(san):
                self.move_text.insert(tk.END, "\n")
        highlighted_tag = f"move_{self.model.displayed_ply}"
        if self.model.displayed_ply > 0:
            self.move_text.tag_configure(
                highlighted_tag,
                background=ACCENT,
                foreground=APP_BACKGROUND,
            )
            ranges = self.move_text.tag_ranges(highlighted_tag)
            if ranges:
                self.move_text.see(ranges[0])
        else:
            self.move_text.see("1.0")
        self.move_text.configure(state=tk.DISABLED)

    def _navigate_start(self) -> None:
        """Pause playback and display the starting position."""
        self._stop_playback()
        if self.model.navigate_start():
            self.status.configure(text="At the starting position")
        self._refresh()

    def _navigate_back(self) -> None:
        """Pause playback and display the previous position."""
        self._stop_playback()
        if self.model.navigate_back():
            self.status.configure(text=f"Position {self.model.displayed_ply}")
        self._refresh()

    def _navigate_forward(self) -> None:
        """Pause playback and display the next position."""
        self._stop_playback()
        if self.model.navigate_forward():
            self.status.configure(text=f"Position {self.model.displayed_ply}")
        self._refresh()

    def _navigate_end(self) -> None:
        """Pause playback and display the final position."""
        self._stop_playback()
        if self.model.navigate_end():
            self.status.configure(text="At the final position")
        self._refresh()

    def _play(self) -> None:
        """Start automatic playback from the displayed position."""
        if self.playback_after_id is not None or not self.model.has_next_position:
            return
        self.status.configure(text="Playing game")
        self._schedule_playback_step()
        self._refresh()

    def _pause(self) -> None:
        """Pause automatic playback immediately."""
        if self._stop_playback():
            self.status.configure(text="Playback paused")
        self._refresh()

    def _schedule_playback_step(self) -> None:
        """Schedule the sole active playback timer using the selected delay."""
        delay_milliseconds = max(1, round(self.playback_seconds.get() * 1000))
        self.playback_after_id = self.after(delay_milliseconds, self._playback_step)

    def _playback_step(self) -> None:
        """Advance one move and schedule the following playback step."""
        self.playback_after_id = None
        self.model.navigate_forward()
        if self.model.has_next_position:
            self._schedule_playback_step()
        else:
            self.status.configure(text="Playback complete")
        self._refresh()

    def _stop_playback(self) -> bool:
        """Cancel the active playback timer, returning whether one existed."""
        if self.playback_after_id is None:
            return False
        self.after_cancel(self.playback_after_id)
        self.playback_after_id = None
        if hasattr(self, "pause_button"):
            self.pause_button.configure(state=tk.DISABLED)
            self.play_button.configure(
                state=tk.NORMAL if self.model.has_next_position else tk.DISABLED
            )
        return True

    def _playback_speed_changed(self, value: str) -> None:
        """Update the user-facing playback delay label."""
        seconds = float(value)
        self.speed_label.configure(text=f"Playback: {seconds:.2f} seconds")
        if self.playback_after_id is not None:
            self.after_cancel(self.playback_after_id)
            self.playback_after_id = None
            self._schedule_playback_step()

    def _undo(self) -> None:
        """Undo the final recorded move."""
        self._stop_playback()
        if self.model.undo():
            self.dirty = True
            self.status.configure(text="Last move removed")
            self._refresh()

    def _clear(self) -> None:
        """Confirm and clear the current game's moves."""
        self._stop_playback()
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
        self._stop_playback()
        self._commit_all_metadata()
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
        self._load_metadata_fields()
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
        self._commit_all_metadata()
        if self.current_path is None:
            return self._save_as()
        return self._write(self.current_path)

    def _save_as(self) -> bool:
        """Prompt for a destination and save the current game."""
        self._commit_all_metadata()
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
        self._stop_playback()
        self._commit_all_metadata()
        if self._may_discard_changes():
            self.destroy()


class CalendarDialog(tk.Toplevel):
    """Application-themed calendar used to choose a PGN date."""

    def __init__(self, parent: PgnEditor, initial_date: date) -> None:
        """Create a modal calendar initially showing a specified date."""
        super().__init__(parent)
        self.result: date | None = None
        self.year = initial_date.year
        self.month = initial_date.month
        self.initial_date = initial_date
        self.withdraw()
        self.title("Choose date")
        self.configure(background=APP_BACKGROUND)
        self.resizable(False, False)
        self.card = ttk.Frame(self, style="Panel.TFrame", padding=20)
        self.card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        header = ttk.Frame(self.card, style="Panel.TFrame")
        header.pack(fill=tk.X, pady=(0, 12))
        ttk.Button(
            header,
            text="◀",
            width=2,
            style="Calendar.TButton",
            command=lambda: self._change_month(-1),
        ).pack(side=tk.LEFT)
        self.month_label = ttk.Label(
            header, text="", style="Section.TLabel", anchor="center"
        )
        self.month_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        ttk.Button(
            header,
            text="▶",
            width=2,
            style="Calendar.TButton",
            command=lambda: self._change_month(1),
        ).pack(side=tk.RIGHT)

        self.days_frame = ttk.Frame(self.card, style="Panel.TFrame")
        self.days_frame.pack(fill=tk.BOTH, expand=True)
        for column, weekday in enumerate(
            ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")
        ):
            self.days_frame.columnconfigure(column, weight=1)
            ttk.Label(
                self.days_frame,
                text=weekday,
                style="Metadata.TLabel",
                anchor="center",
            ).grid(row=0, column=column, sticky="ew", padx=2, pady=(0, 5))

        ttk.Button(
            self.card,
            text="Today",
            command=lambda: self._choose(datetime.now(UTC).astimezone().date()),
        ).pack(fill=tk.X, pady=(12, 0))
        self._render_month()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda event: self.destroy())
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_reqwidth()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_reqheight()) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")
        self.deiconify()
        self.grab_set()

    def _render_month(self) -> None:
        """Render the currently selected month into the day grid."""
        self.month_label.configure(
            text=date(self.year, self.month, 1).strftime("%B %Y")
        )
        for child in self.days_frame.grid_slaves():
            if int(child.grid_info()["row"]) > 0:
                child.destroy()
        for row, week in enumerate(
            Calendar(firstweekday=0).monthdayscalendar(self.year, self.month), start=1
        ):
            for column, day_number in enumerate(week):
                if day_number == 0:
                    continue
                selected_date = date(self.year, self.month, day_number)
                style = (
                    "Accent.TButton"
                    if selected_date == self.initial_date
                    else "Calendar.TButton"
                )
                ttk.Button(
                    self.days_frame,
                    text=str(day_number),
                    width=3,
                    style=style,
                    command=lambda value=selected_date: self._choose(value),
                ).grid(row=row, column=column, sticky="nsew", padx=2, pady=2)

    def _change_month(self, offset: int) -> None:
        """Move the calendar backwards or forwards by one month."""
        month_index = self.year * 12 + self.month - 1 + offset
        self.year, zero_based_month = divmod(month_index, 12)
        self.month = zero_based_month + 1
        self._render_month()

    def _choose(self, selected_date: date) -> None:
        """Store the chosen date and close the calendar."""
        self.result = selected_date
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
