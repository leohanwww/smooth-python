异常类的部分层次结构

BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
├── StopIteration
├── ArithmeticError
│ ├── FloatingPointError
│ ├── OverflowError
│ └── ZeroDivisionError
├── AssertionError
├── AttributeError
├── BufferError
├── EOFError
├── ImportError
├── LookupError 
│ ├── IndexError 
│ └── KeyError 
├── MemoryError
... etc.