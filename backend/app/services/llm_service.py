"""LLM服务模块"""

from ..config import get_settings
from langchain_openai import ChatOpenAI
import os


# 全局LLM实例
_llm_instance = None


def get_llm():
    """
    获取LLM实例(单例模式)
    """
    global _llm_instance
    
    if _llm_instance is None:
        settings = get_settings()
        _llm_instance = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            base_url= settings.openai_base_url,
            timeout=60,
            streaming=True,
            temperature=0,
        )
        
        print(f"✅ LLM服务初始化成功")
        print(f"   模型: {os.getenv('OPENAI_MODEL')}")  # 建议改为 OPENAI_MODEL

        # ====== 在这里添加包装代码 ======
        import functools
        import json

        def ensure_string_content(messages):
            for msg in messages:
                if hasattr(msg, 'content') and not isinstance(msg.content, str):
                    if hasattr(msg, 'type') and msg.type == 'tool':
                        msg.content = json.dumps(msg.content, ensure_ascii=False)
                    else:
                        msg.content = str(msg.content)
            return messages

        original_ainvoke = _llm_instance.ainvoke

        @functools.wraps(original_ainvoke)
        async def safe_ainvoke(input, config=None, **kwargs):
            if isinstance(input, dict) and 'messages' in input:
                input['messages'] = ensure_string_content(input['messages'])
            elif isinstance(input, list):
                input = ensure_string_content(input)
            return await original_ainvoke(input, config, **kwargs)

        _llm_instance.ainvoke = safe_ainvoke
        # ====== 包装代码结束 ======
    
    return _llm_instance


def reset_llm():
    """重置LLM实例(用于测试或重新配置)"""
    global _llm_instance
    _llm_instance = None
