from enum import auto

from sqlglot.helper import AutoName


class TokenType(AutoName):
    PAREN = auto()
    L_PAREN = auto()
    R_PAREN = auto()
    BRACKET = auto()
    L_BRACKET = auto()
    R_BRACKET = auto()
    L_BRACE = auto()
    R_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    DASH = auto()
    PLUS = auto()
    COLON = auto()
    SEMICOLON = auto()
    STAR = auto()
    SLASH = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()
    NOT = auto()
    EQ = auto()
    NEQ = auto()
    AND = auto()
    OR = auto()
    AMP = auto()
    PIPE = auto()
    CARET = auto()
    TILDA = auto()
    LSHIFT = auto()
    RSHIFT = auto()

    SPACE = auto()
    BREAK = auto()

    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    COLUMN = auto()
    TABLE = auto()
    VAR = auto()

    # types
    BOOLEAN = auto()
    TINYINT = auto()
    SMALLINT = auto()
    INT = auto()
    BIGINT = auto()
    FLOAT = auto()
    DOUBLE = auto()
    DECIMAL = auto()
    CHAR = auto()
    VARCHAR = auto()
    TEXT = auto()
    BINARY = auto()
    JSON = auto()
    TIMESTAMP = auto()
    DATE = auto()

    # keywords
    ALIAS = auto()
    ALL = auto()
    ARRAY = auto()
    ASC = auto()
    BETWEEN = auto()
    BY = auto()
    CASE = auto()
    CAST = auto()
    COUNT = auto()
    COMMENT = auto()
    COMMENT_END = auto()
    COMMENT_START = auto()
    CREATE = auto()
    CROSS = auto()
    CURRENT_ROW = auto()
    DESC = auto()
    DISTINCT = auto()
    DROP = auto()
    ELSE = auto()
    END = auto()
    EXISTS = auto()
    FOLLOWING = auto()
    FORMAT = auto()
    FULL = auto()
    FUNC = auto()
    FROM = auto()
    GROUP = auto()
    HAVING = auto()
    HINT = auto()
    IF = auto()
    IN = auto()
    INNER = auto()
    INTERVAL = auto()
    IS = auto()
    JOIN = auto()
    LATERAL = auto()
    LEFT = auto()
    LIKE = auto()
    LIMIT = auto()
    MAP = auto()
    MOD = auto()
    NULL = auto()
    ON = auto()
    ORDER = auto()
    ORDINALITY = auto()
    OUTER = auto()
    OVER = auto()
    PARTITION = auto()
    PRECEDING = auto()
    RANGE = auto()
    RIGHT = auto()
    RLIKE = auto()
    ROWS = auto()
    SELECT = auto()
    SPEC = auto()
    STORED = auto()
    THEN = auto()
    UNBOUNDED = auto()
    UNION = auto()
    UNNEST = auto()
    VIEW = auto()
    WHEN = auto()
    WHERE = auto()
    WITH = auto()


class Token:
    @classmethod
    def number(cls, number):
        return cls(TokenType.NUMBER, f"{number}")

    @classmethod
    def string(cls, string):
        return cls(TokenType.STRING, f"'{string}'")

    def __init__(self, token_type, text, line=0, col=0):
        self.token_type = token_type
        self.text = text
        self.line = line
        self.col = col - len(text)
        self.parent = None
        self.arg_key = None

    def __repr__(self):
        attributes = ", ".join([
            f"{k}: {v}"
            for k, v in self.__dict__.items()
            if k != 'parent'
        ])
        return f"<Token {attributes}>"

    def to_s(self, _level=0):
        return self.text

class Tokenizer:
    SINGLE_TOKENS = {
        '(': TokenType.L_PAREN,
        ')': TokenType.R_PAREN,
        '[': TokenType.L_BRACKET,
        ']': TokenType.R_BRACKET,
        '{': TokenType.L_BRACE,
        '}': TokenType.R_BRACE,
        '&': TokenType.AMP,
        '^': TokenType.CARET,
        ':': TokenType.COLON,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        '-': TokenType.DASH,
        '=': TokenType.EQ,
        '>': TokenType.GT,
        '<': TokenType.LT,
        '%': TokenType.MOD,
        '!': TokenType.NOT,
        '|': TokenType.PIPE,
        '+': TokenType.PLUS,
        ';': TokenType.SEMICOLON,
        '/': TokenType.SLASH,
        '*': TokenType.STAR,
        '~': TokenType.TILDA,
    }

    KEYWORDS = {
        '/*+': TokenType.HINT,
        '--': TokenType.COMMENT,
        '/*': TokenType.COMMENT_START,
        '*/': TokenType.COMMENT_END,
        '>=': TokenType.GTE,
        '<=': TokenType.LTE,
        '<>': TokenType.NEQ,
        '!=': TokenType.NEQ,
        '<<': TokenType.LSHIFT,
        '>>': TokenType.RSHIFT,

        'ALL': TokenType.ALL,
        'AND': TokenType.AND,
        'ASC': TokenType.ASC,
        'AS': TokenType.ALIAS,
        'BETWEEN': TokenType.BETWEEN,
        'BY': TokenType.BY,
        'CASE': TokenType.CASE,
        'CAST': TokenType.CAST,
        'COUNT': TokenType.COUNT,
        'CREATE': TokenType.CREATE,
        'CROSS': TokenType.CROSS,
        'CURRENT ROW': TokenType.CURRENT_ROW,
        'DESC': TokenType.DESC,
        'DISTINCT': TokenType.DISTINCT,
        'DROP': TokenType.DROP,
        'ELSE': TokenType.ELSE,
        'END': TokenType.END,
        'EXISTS': TokenType.EXISTS,
        'FORMAT': TokenType.FORMAT,
        'FULL': TokenType.FULL,
        'FOLLOWING': TokenType.FOLLOWING,
        'FROM': TokenType.FROM,
        'GROUP BY': TokenType.GROUP,
        'HAVING': TokenType.HAVING,
        'IF': TokenType.IF,
        'IN': TokenType.IN,
        'INNER': TokenType.INNER,
        'INTERVAL': TokenType.INTERVAL,
        'IS': TokenType.IS,
        'JOIN': TokenType.JOIN,
        'LATERAL': TokenType.LATERAL,
        'LEFT': TokenType.LEFT,
        'LIKE': TokenType.LIKE,
        'LIMIT': TokenType.LIMIT,
        'NOT': TokenType.NOT,
        'NULL': TokenType.NULL,
        'ON': TokenType.ON,
        'OR': TokenType.OR,
        'ORDER BY': TokenType.ORDER,
        'ORDINALITY': TokenType.ORDINALITY,
        'OUTER': TokenType.OUTER,
        'OVER': TokenType.OVER,
        'PARTITION BY': TokenType.PARTITION,
        'PRECEDING': TokenType.PRECEDING,
        'RANGE': TokenType.RANGE,
        'RIGHT': TokenType.RIGHT,
        'RLIKE': TokenType.RLIKE,
        'ROWS': TokenType.ROWS,
        'SELECT': TokenType.SELECT,
        'STORED': TokenType.STORED,
        'TABLE': TokenType.TABLE,
        'THEN': TokenType.THEN,
        'UNBOUNDED': TokenType.UNBOUNDED,
        'UNION': TokenType.UNION,
        'UNNEST': TokenType.UNNEST,
        'VIEW': TokenType.VIEW,
        'WHEN': TokenType.WHEN,
        'WHERE': TokenType.WHERE,
        'WITH': TokenType.WITH,

        'ARRAY': TokenType.ARRAY,
        'BOOL': TokenType.BOOLEAN,
        'BOOLEAN': TokenType.BOOLEAN,
        'TINYINT': TokenType.TINYINT,
        'SMALLINT': TokenType.SMALLINT,
        'INT2': TokenType.SMALLINT,
        'INTEGER': TokenType.INT,
        'INT': TokenType.INT,
        'INT4': TokenType.INT,
        'BIGINT': TokenType.BIGINT,
        'INT8': TokenType.BIGINT,
        'DECIMAL': TokenType.DECIMAL,
        'MAP': TokenType.MAP,
        'NUMERIC': TokenType.DECIMAL,
        'DEC': TokenType.DECIMAL,
        'FIXED': TokenType.DECIMAL,
        'REAL': TokenType.FLOAT,
        'FLOAT': TokenType.FLOAT,
        'FLOAT4': TokenType.FLOAT,
        'FLOAT8': TokenType.DOUBLE,
        'DOUBLE': TokenType.DOUBLE,
        'JSON': TokenType.JSON,
        'CHAR': TokenType.CHAR,
        'VARCHAR': TokenType.VARCHAR,
        'STRING': TokenType.TEXT,
        'TEXT': TokenType.TEXT,
        'BINARY': TokenType.BINARY,
        'TIMESTAMP': TokenType.TIMESTAMP,
        'DATE': TokenType.DATE,
    }

    WHITE_SPACE = {
        ' ': TokenType.SPACE,
        "\t": TokenType.SPACE,
        "\n": TokenType.BREAK,
        "\r": TokenType.BREAK,
        "\rn": TokenType.BREAK,
    }

    ESCAPE_CODE = '__sqlglot_escape__'

    def __init__(self, **opts):
        self.quote = opts.get('quote') or "'"
        self.identifier = opts.get('identifier') or '"'
        self.escape = opts.get('escape') or "'"
        self.single_tokens = {**self.SINGLE_TOKENS, **opts.get('single_tokens', {})}
        self.keywords = {**self.KEYWORDS, **opts.get('keywords', {})}
        self.white_space = {**self.WHITE_SPACE, **opts.get('white_space', {})}
        self.reset()

    def reset(self):
        self.code = ''
        self.size = 0
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 0
        self._col = 0

    def tokenize(self, code): # pylint: disable=too-many-branches
        self.reset()
        self.code = code
        self.size = len(code)

        ambiguous = {
            key: self.keywords[key]
            for key in sorted(self.keywords, key=lambda k: -len(k))
            if self.keywords[key] not in (TokenType.COMMENT, TokenType.COMMENT_START)
            and (' ' in key or any(single in key for single in self.single_tokens))
        }

        comments = {
            token: key
            for key, token in self.keywords.items()
            if token in (TokenType.COMMENT, TokenType.COMMENT_START, TokenType.COMMENT_END)
        }

        while not self._end:
            self._start = self._current
            self._advance()

            if self._scan_ambiguous(ambiguous):
                pass
            elif self._scan_comments(comments):
                pass
            elif self._char in self.single_tokens:
                self._add(self.single_tokens[self._char])
            elif self._char in self.WHITE_SPACE:
                white_space = self.WHITE_SPACE[self._char]
                if white_space == TokenType.BREAK:
                    self._col = 0
                    self._line += 1
            elif self._char.isdigit():
                self._scan_number()
            elif self._char == self.quote:
                self._scan_string()
            elif self._char == self.identifier:
                self._scan_identifier()
            else:
                self._scan_var()

        return self.tokens

    @property
    def _char(self):
        if self._current - 1 < self.size:
            return self.code[self._current - 1]
        return ''

    def _chars(self, size):
        start = self._current - 1
        end = start + size
        if end < self.size:
            return self.code[start:end].upper()
        return ''

    @property
    def _text(self):
        return self.code[self._start:self._current]

    @property
    def _peek(self):
        if not self._end:
            return self.code[self._current]
        return ''

    @property
    def _end(self):
        return self._current >= self.size

    def _advance(self, i=1):
        self._col += i
        self._current += i

    def _add(self, token_type, text=None):
        self.tokens.append(Token(token_type, text or self._text, self._line, self._col))

    def _scan_ambiguous(self, ambiguous):
        for key, token in ambiguous.items():
            size = len(key)
            if self._chars(size) == key:
                self._advance(size - 1)
                self._add(token)
                return True
        return False

    def _scan_comments(self, comments):
        comment = comments[TokenType.COMMENT]

        if self._chars(len(comment)) == comment:
            while not self._end and self.WHITE_SPACE.get(self._char) != TokenType.BREAK:
                self._advance()
            return True

        comment_start = comments[TokenType.COMMENT_START]
        comment_end = comments[TokenType.COMMENT_END]

        if self._chars(len(comment_start)) == comment_start:
            size = len(comment_end)
            while not self._end and self._chars(size) != comment_end:
                self._advance()
            self._advance(size - 1)
            return True
        return False

    def _scan_number(self):
        while self._peek.isdigit() or self._peek == '.':
            self._advance()
        self._add(TokenType.NUMBER)

    def _scan_string(self):
        text = []

        while True:
            if self._end:
                raise RuntimeError(f"Missing {self.quote} from {self._line}:{self._start}")
            text.append(self._char)
            self._advance()

            if self.escape and self._char == self.escape and self._peek == self.quote:
                text.append(self.ESCAPE_CODE)
                self._advance()
            elif self._char == self.quote:
                break

        text.append(self._char)
        self._add(TokenType.STRING, ''.join(text))

    def _scan_identifier(self):
        while self._peek != self.identifier:
            if self._end:
                raise RuntimeError(f"Missing {self.identifier} from {self._line}:{self._start}")
            self._advance()
        self._advance()
        self._add(TokenType.IDENTIFIER)

    def _scan_var(self):
        while True:
            char = self._peek.strip()
            if char and char not in self.single_tokens:
                self._advance()
            else:
                break
        self._add(self.keywords.get(self._text.upper(), TokenType.VAR))
