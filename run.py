from src.classifier import load_categories, classify_customer_query
from datetime import datetime

def main():
    print("=== 客户问题分类系统 ===")
    print("输入 'quit' 退出程序\n")

    # 加载类别
    try:
        categories = load_categories()
        print(f"已加载 {len(categories)} 个法律类别。\n")
    except Exception as e:
        print(f"初始化失败: {e}")
        return

    # 交互式分类
    while True:
        
        query = input("请输入客户问题: ").strip()
        if query.lower() == 'quit':
            print("再见！")
            break
        if not query:
            print("问题不能为空，请重新输入。\n")
            continue

        try:
            start = datetime.now()
            result = classify_customer_query(query, categories)
            print(f"【分类结果】{result}\n")
            end = datetime.now()
            cost = (end - start).total_seconds()
            print(f"Execution time: {cost} seconds")
        except Exception as e:
            print(f"分类出错: {e}\n")


if __name__ == "__main__":
    main()