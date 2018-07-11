#encoding:utf-8
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    #日志级别，日志格式，输出位置
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(pathname)s[%(lineno)d] %(levelname)s:%(message)s",
                        filename="log.txt")
    logger.debug('I am Debug')
    logger.info('I am info')
    logger.error('I am error')