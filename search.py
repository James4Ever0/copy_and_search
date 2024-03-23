from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh.index import create_in
from whoosh.writing import SegmentWriter
from whoosh.index import open_dir
from whoosh.sorting import FieldFacet
from jieba.analyse import ChineseAnalyzer
import os
from config import APP_CONFIG, SEARCH_LIMIT
import shutil

def get_or_create_index():
    index_path = APP_CONFIG["index_directory"]
    analyser = ChineseAnalyzer()
    schema = Schema(
        title=TEXT(stored=True, analyzer=analyser),
        content=TEXT(stored=True, analyzer=analyser),
    )

    # 索引路径不存在则创建,存在则调用open_dir方法打开索引
    if not os.path.exists(index_path):
        os.mkdir(index_path)
        # 使用create_in方法创建索引，index_path为索引路径，schema为前面定义的索引字段，indexname为索引名称（根据需要进行修改）
        ix = create_in(index_path, schema=schema, indexname="indexname")
    else:
        ix = open_dir(index_path, indexname="indexname")
    return ix


SEARCH_INDEX = get_or_create_index()


def remove_and_create_index():
    global SEARCH_INDEX
    SEARCH_INDEX.close()
    index_path = APP_CONFIG["index_directory"]
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    SEARCH_INDEX = get_or_create_index()


def search_by_query(query: str):
    global SEARCH_INDEX
    ret = []
    with SEARCH_INDEX.searcher() as searcher:
        # 单关键词搜索
        # parser = QueryParser("title", ix.schema).parse("手册")

        # 多关键词同时搜索
        parser = MultifieldParser(["title", "content"], SEARCH_INDEX.schema).parse(
            query
        )

        # 对结果进行排序
        facet = FieldFacet("content", reverse=True)

        # limit为搜索结果的限制，默认为10，None为不限制。sortedby为排序规则
        results = searcher.search(
            parser, limit=SEARCH_LIMIT, sortedby=facet, terms=True
        )

        # 打印搜索结果
        for i in results:
            # Get the 'content' field as a string
            content_str = i["content"]
            ret.append(content_str)
    return ret


def add_document_by_file_relpath_and_line_content(file_relpath: str, line_content: str
):
    line_content = line_content.strip()
    if line_content:
        # 使用add_document向索引内添加内容
        writer: SegmentWriter = SEARCH_INDEX.writer()
        writer.add_document(title=file_relpath, content=line_content)
        # 提交
        writer.commit()


def refresh_index():
    global SEARCH_INDEX
    remove_and_create_index()
    document_directory = APP_CONFIG["document_directory"]
    # recursively walk over directory and index all files


    for dirpath, _, filenames in os.walk(document_directory):
        for filename in filenames:
            file_relpath = os.path.join(dirpath, filename)
            file_abspath = os.path.join(document_directory, filename)
            if file_relpath.split(".")[-1] == "txt":
                print(f"[search] processing file: {file_abspath}")
                with open(file_abspath, "r") as f:
                    for line_content in f.readlines():
                        add_document_by_file_relpath_and_line_content(file_relpath, line_content
                        )
            else:
                print(f"[search] skipping file: {file_abspath}")