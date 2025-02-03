import logging
import colorlog
from enum import Enum
from typing import Optional

class LogType(Enum):
    """日志类型枚举，定义不同类型日志的级别和颜色"""
    USER_INPUT = (logging.DEBUG, 'blue', '用户输入')          # 蓝色
    REQUEST = (logging.INFO, 'green', '请求数据')            # 绿色
    RESPONSE = (logging.WARNING, 'yellow', '原始响应')       # 黄色
    FUNCTION_CALL = (logging.ERROR, 'red', '函数调用信息')   # 红色
    FUNCTION_RESULT = (logging.CRITICAL, 'red,bg_white', '函数执行结果')  # 红底白字
    ERROR = (logging.ERROR, 'red', '错误信息')              # 红色
    TIMING = (logging.INFO, 'green', '执行耗时')            # 绿色

    def __init__(self, level, color, title):
        self.level = level
        self.color = color
        self.title = title

def setup_logger(debug: bool = True) -> Optional[logging.Logger]:
    """设置彩色日志
    Args:
        debug: 是否启用调试模式
    Returns:
        logger: 配置好的日志器，如果debug=False则返回None
    """
    if not debug:
        return None
        
    logger = colorlog.getLogger('gpt_caller')
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] %(message)s%(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': LogType.USER_INPUT.color,
                'INFO': LogType.REQUEST.color,
                'WARNING': LogType.RESPONSE.color,
                'ERROR': LogType.FUNCTION_CALL.color,
                'CRITICAL': LogType.FUNCTION_RESULT.color,
            }
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

def log_debug(logger: Optional[logging.Logger], log_type: LogType, content: any) -> None:
    """输出调试信息，使用彩色输出
    Args:
        logger: 日志器
        log_type: 日志类型
        content: 日志内容
    """
    if not logger:
        return
        
    # 输出带颜色的标题
    logger.log(log_type.level, f"\n{'='*50}")
    logger.log(log_type.level, f"=== {log_type.title} ===")
    logger.log(log_type.level, f"{'='*50}\n")
    
    # 输出内容
    if isinstance(content, str):
        logger.log(log_type.level, content)
    else:
        import json
        logger.log(
            log_type.level,
            json.dumps(content, indent=2, ensure_ascii=False)
        )
    
    # 输出分隔符
    logger.log(log_type.level, f"\n{'='*50}\n") 