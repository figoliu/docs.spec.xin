#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
搜索索引优化模块 - 关联需求FR-007

此模块提供静态文档站点的搜索索引优化功能，包括：
1. 中文分词支持
2. 索引构建和优化
3. 搜索结果排序算法
4. 搜索建议和自动完成
5. 索引定期更新机制
"""

import os
import json
import re
import time
import hashlib
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime

class SearchIndexOptimizer:
    """搜索索引优化器类"""
    
    def __init__(self, docs_dir: str = None, index_dir: str = None):
        """初始化搜索索引优化器
        
        Args:
            docs_dir: 文档目录路径，默认为docs目录
            index_dir: 索引目录路径，默认为.config/index目录
        """
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.docs_dir = docs_dir or os.path.join(self.project_root, 'docs')
        self.index_dir = index_dir or os.path.join(self.project_root, '.config', 'index')
        self.index_file = os.path.join(self.index_dir, 'search_index.json')
        self.metadata_file = os.path.join(self.index_dir, 'index_metadata.json')
        
        # 确保索引目录存在
        self._ensure_index_directory()
        
        # 初始化索引和元数据
        self._index = {}
        self._metadata = {}
        self._load_index()
        self._load_metadata()
    
    def _ensure_index_directory(self):
        """确保索引目录存在"""
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
    
    def _load_index(self):
        """加载搜索索引"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self._index = json.load(f)
                print(f"已加载搜索索引，包含 {len(self._index)} 个文档")
            except Exception as e:
                print(f"加载搜索索引失败: {e}")
                self._index = {}
    
    def _load_metadata(self):
        """加载索引元数据"""
        default_metadata = {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "version": "1.0",
            "document_count": 0,
            "token_count": 0,
            "languages": ["zh", "en"],
            "optimization_settings": {
                "stemming": True,
                "stop_words_removal": True,
                "synonyms_enabled": True,
                "chinese_segmentation": True,
                "max_tokens_per_document": 10000,
                "min_token_length": 2
            }
        }
        
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self._metadata = json.load(f)
            except Exception as e:
                print(f"加载索引元数据失败: {e}")
                self._metadata = default_metadata
        else:
            self._metadata = default_metadata
    
    def _save_index(self):
        """保存搜索索引"""
        try:
            self._ensure_index_directory()
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self._index, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存搜索索引失败: {e}")
            return False
    
    def _save_metadata(self):
        """保存索引元数据"""
        try:
            self._ensure_index_directory()
            self._metadata["last_updated"] = datetime.now().isoformat()
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self._metadata, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存索引元数据失败: {e}")
            return False
    
    def _extract_text_from_markdown(self, markdown_content: str) -> str:
        """从Markdown内容中提取纯文本
        
        Args:
            markdown_content: Markdown格式的文本
            
        Returns:
            提取后的纯文本
        """
        # 移除代码块
        text = re.sub(r'```[\s\S]*?```', '', markdown_content)
        # 移除行内代码
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # 移除链接，但保留链接文本
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        # 移除图片
        text = re.sub(r'!\[(.*?)\]\(.*?\)', '', text)
        # 移除标题标记
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        # 移除列表标记
        text = re.sub(r'^[\s]*[-*+]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*\d+\.\s*', '', text, flags=re.MULTILINE)
        # 移除强调标记
        text = re.sub(r'[*_]{1,3}([^\s][^*_]*[^\s])[*_]{1,3}', r'\1', text)
        # 移除表格
        text = re.sub(r'\|.*?\|\s*\n', '', text)
        # 移除水平分隔线
        text = re.sub(r'^[-=*]{3,}\s*\n', '', text, flags=re.MULTILINE)
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除注释
        text = re.sub(r'<!--[\s\S]*?-->', '', text)
        
        return text.strip()
    
    def _tokenize(self, text: str) -> List[str]:
        """将文本分词
        
        Args:
            text: 要分词的文本
            
        Returns:
            词语列表
        """
        tokens = []
        
        # 中文分词（简化版，实际项目中可使用jieba等专业分词库）
        if self._metadata["optimization_settings"]["chinese_segmentation"]:
            # 匹配中文词语
            chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
            chinese_matches = chinese_pattern.finditer(text)
            
            last_end = 0
            for match in chinese_matches:
                start, end = match.span()
                # 处理非中文字符
                non_chinese = text[last_end:start].strip()
                if non_chinese:
                    tokens.extend(self._tokenize_non_chinese(non_chinese))
                # 添加中文词语
                chinese_word = match.group()
                # 对于长的中文词语，简单地按单个字符切分
                if len(chinese_word) <= 2:
                    tokens.append(chinese_word)
                else:
                    # 保留完整词和单字
                    tokens.append(chinese_word)
                    tokens.extend(list(chinese_word))
                last_end = end
            
            # 处理剩余的非中文字符
            remaining = text[last_end:].strip()
            if remaining:
                tokens.extend(self._tokenize_non_chinese(remaining))
        else:
            # 只进行非中文分词
            tokens.extend(self._tokenize_non_chinese(text))
        
        # 应用停用词过滤
        if self._metadata["optimization_settings"]["stop_words_removal"]:
            tokens = self._remove_stop_words(tokens)
        
        # 过滤短词
        min_length = self._metadata["optimization_settings"]["min_token_length"]
        tokens = [token for token in tokens if len(token) >= min_length]
        
        return tokens
    
    def _tokenize_non_chinese(self, text: str) -> List[str]:
        """非中文文本分词
        
        Args:
            text: 非中文文本
            
        Returns:
            词语列表
        """
        # 提取字母、数字组成的词语
        tokens = re.findall(r'[a-zA-Z0-9]+', text)
        return tokens
    
    def _remove_stop_words(self, tokens: List[str]) -> List[str]:
        """移除停用词
        
        Args:
            tokens: 词语列表
            
        Returns:
            过滤后的词语列表
        """
        # 简单的停用词列表（中英文）
        stop_words = {
            '的', '了', '和', '是', '在', '有', '我', '他', '她', '它', '你',
            '这', '那', '个', '我们', '你们', '他们', '她们', '它们',
            'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'for',
            'with', 'on', 'in', 'at', 'to', 'of', 'by', 'from', 'as', 'is',
            'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
        }
        
        return [token for token in tokens if token.lower() not in stop_words]
    
    def build_index(self, force_rebuild: bool = False) -> bool:
        """构建搜索索引
        
        Args:
            force_rebuild: 是否强制重新构建
            
        Returns:
            是否构建成功
        """
        print(f"开始构建搜索索引，文档目录: {self.docs_dir}")
        
        if not force_rebuild and self._index:
            # 检查是否需要更新
            needs_update = False
            for root, _, files in os.walk(self.docs_dir):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        file_rel_path = os.path.relpath(file_path, self.docs_dir)
                        file_mtime = os.path.getmtime(file_path)
                        
                        # 检查文件是否存在于索引中或是否已修改
                        if file_rel_path not in self._index or \
                           'modified_time' not in self._index[file_rel_path] or \
                           file_mtime > self._index[file_rel_path]['modified_time']:
                            needs_update = True
                            break
                if needs_update:
                    break
            
            if not needs_update:
                print("搜索索引已是最新，无需更新")
                return True
        
        # 重新初始化索引
        new_index = {}
        processed_docs = 0
        total_tokens = 0
        
        # 遍历文档目录
        for root, _, files in os.walk(self.docs_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    file_rel_path = os.path.relpath(file_path, self.docs_dir)
                    file_mtime = os.path.getmtime(file_path)
                    
                    try:
                        # 读取文件内容
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 提取纯文本
                        text = self._extract_text_from_markdown(content)
                        
                        # 分词
                        tokens = self._tokenize(text)
                        
                        # 限制每个文档的token数量
                        max_tokens = self._metadata["optimization_settings"]["max_tokens_per_document"]
                        tokens = tokens[:max_tokens]
                        
                        # 创建文档索引
                        doc_index = {
                            'title': self._extract_title(content),
                            'path': file_rel_path,
                            'content': text[:1000],  # 保存前1000个字符作为摘要
                            'tokens': tokens,
                            'token_count': len(tokens),
                            'modified_time': file_mtime,
                            'created_at': datetime.now().isoformat()
                        }
                        
                        # 建立倒排索引
                        inverted_index = {}
                        for token in tokens:
                            if token not in inverted_index:
                                inverted_index[token] = 0
                            inverted_index[token] += 1
                        
                        doc_index['inverted_index'] = inverted_index
                        new_index[file_rel_path] = doc_index
                        
                        processed_docs += 1
                        total_tokens += len(tokens)
                        
                        if processed_docs % 10 == 0:
                            print(f"已处理 {processed_docs} 个文档...")
                            
                    except Exception as e:
                        print(f"处理文件 {file_rel_path} 失败: {e}")
        
        # 保存索引
        self._index = new_index
        
        # 更新元数据
        self._metadata["document_count"] = processed_docs
        self._metadata["token_count"] = total_tokens
        self._metadata["last_updated"] = datetime.now().isoformat()
        
        # 保存索引和元数据
        if self._save_index() and self._save_metadata():
            print(f"搜索索引构建完成！处理了 {processed_docs} 个文档，索引了 {total_tokens} 个词语")
            return True
        else:
            print("搜索索引构建失败")
            return False
    
    def _extract_title(self, content: str) -> str:
        """从Markdown内容中提取标题
        
        Args:
            content: Markdown格式的文本
            
        Returns:
            提取的标题
        """
        # 查找一级标题
        match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # 如果没有一级标题，尝试从文件内容开头提取
        first_lines = content.split('\n')[:3]
        for line in first_lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('```'):
                return stripped[:100]  # 限制标题长度
        
        return "未命名文档"
    
    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """搜索文档
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            搜索结果列表
        """
        if not self._index:
            print("搜索索引为空，请先构建索引")
            return []
        
        if not query.strip():
            return []
        
        # 分词查询
        query_tokens = self._tokenize(query)
        
        # 计算文档得分
        results = []
        for doc_path, doc_data in self._index.items():
            score = self._calculate_relevance_score(query_tokens, doc_data)
            if score > 0:
                # 生成摘要片段
                snippet = self._generate_snippet(query, doc_data['content'])
                
                results.append({
                    'path': doc_path,
                    'title': doc_data['title'],
                    'snippet': snippet,
                    'score': score,
                    'modified_time': doc_data['modified_time']
                })
        
        # 按相关性得分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance_score(self, query_tokens: List[str], doc_data: Dict[str, Any]) -> float:
        """计算文档与查询的相关性得分
        
        Args:
            query_tokens: 查询词语列表
            doc_data: 文档数据
            
        Returns:
            相关性得分
        """
        if not query_tokens:
            return 0
        
        score = 0.0
        doc_tokens = set(doc_data['tokens'])
        doc_inverted_index = doc_data.get('inverted_index', {})
        
        # 基础得分：查询词出现在文档中的比例
        matched_tokens = set(query_tokens) & doc_tokens
        base_score = len(matched_tokens) / len(set(query_tokens))
        
        # 词频加权
        term_frequency_score = 0
        for token in matched_tokens:
            if token in doc_inverted_index:
                # 归一化词频
                tf = doc_inverted_index[token] / doc_data['token_count'] if doc_data['token_count'] > 0 else 0
                term_frequency_score += tf
        
        # 文档长度归一化（短文档优先）
        length_normalization = 1.0 / (1.0 + doc_data['token_count'] / 1000.0)
        
        # 综合得分
        score = (base_score * 0.6 + term_frequency_score * 0.4) * length_normalization
        
        return score
    
    def _generate_snippet(self, query: str, content: str, max_length: int = 200) -> str:
        """生成搜索结果摘要
        
        Args:
            query: 搜索查询
            content: 文档内容
            max_length: 摘要最大长度
            
        Returns:
            格式化的摘要
        """
        # 简化的摘要生成，实际项目中可以使用更复杂的算法
        # 尝试找到查询词附近的文本
        query_lower = query.lower()
        content_lower = content.lower()
        
        start_pos = content_lower.find(query_lower)
        if start_pos >= 0:
            # 找到查询词，提取其前后的文本
            snippet_start = max(0, start_pos - max_length // 2)
            snippet_end = min(len(content), start_pos + len(query) + max_length // 2)
            
            snippet = content[snippet_start:snippet_end]
            # 添加省略号
            if snippet_start > 0:
                snippet = "..." + snippet
            if snippet_end < len(content):
                snippet = snippet + "..."
        else:
            # 未找到查询词，使用文档开头
            snippet = content[:max_length]
            if len(content) > max_length:
                snippet = snippet + "..."
        
        # 高亮查询词
        for token in self._tokenize(query):
            # 使用不区分大小写的替换
            pattern = re.compile(re.escape(token), re.IGNORECASE)
            snippet = pattern.sub(f"<mark>{token}</mark>", snippet)
        
        return snippet
    
    def get_search_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """获取搜索建议
        
        Args:
            query: 部分搜索查询
            limit: 返回建议数量限制
            
        Returns:
            搜索建议列表
        """
        if not self._index or not query.strip():
            return []
        
        query_lower = query.lower()
        suggestions = set()
        
        # 从文档标题和内容中提取建议
        for doc_data in self._index.values():
            # 检查标题
            title_lower = doc_data['title'].lower()
            if query_lower in title_lower:
                suggestions.add(doc_data['title'])
            
            # 检查内容中的词语
            for token in doc_data['tokens']:
                token_lower = token.lower()
                if token_lower.startswith(query_lower) and len(token) > len(query):
                    suggestions.add(token)
            
            # 如果建议数量足够，提前返回
            if len(suggestions) >= limit:
                break
        
        # 按相关性排序（这里简单按长度排序）
        sorted_suggestions = sorted(suggestions, key=lambda x: (len(x), x))
        
        return sorted_suggestions[:limit]
    
    def optimize_index(self):
        """优化搜索索引
        
        包括：
        1. 合并重复索引项
        2. 清理无效条目
        3. 优化索引结构
        """
        print("开始优化搜索索引...")
        
        # 清理无效条目
        valid_index = {}
        invalid_count = 0
        
        for doc_path, doc_data in self._index.items():
            full_path = os.path.join(self.docs_dir, doc_path)
            # 检查文件是否存在
            if os.path.exists(full_path):
                # 更新修改时间
                doc_data['modified_time'] = os.path.getmtime(full_path)
                valid_index[doc_path] = doc_data
            else:
                invalid_count += 1
        
        # 保存优化后的索引
        self._index = valid_index
        self._metadata["document_count"] = len(self._index)
        
        if self._save_index() and self._save_metadata():
            print(f"搜索索引优化完成！清理了 {invalid_count} 个无效条目")
            return True
        else:
            print("搜索索引优化失败")
            return False
    
    def schedule_index_update(self, interval_seconds: int = 3600):
        """安排定期索引更新
        
        Args:
            interval_seconds: 更新间隔（秒），默认1小时
        """
        print(f"已设置定期索引更新，间隔: {interval_seconds} 秒")
        
        try:
            while True:
                time.sleep(interval_seconds)
                print("执行定期索引更新...")
                self.build_index()
        except KeyboardInterrupt:
            print("定期索引更新已停止")
    
    def export_index_stats(self) -> Dict[str, Any]:
        """导出索引统计信息
        
        Returns:
            索引统计信息
        """
        # 计算词语频率
        token_frequency = {}
        for doc_data in self._index.values():
            for token, count in doc_data.get('inverted_index', {}).items():
                if token not in token_frequency:
                    token_frequency[token] = 0
                token_frequency[token] += count
        
        # 获取最常见的词语
        top_tokens = sorted(token_frequency.items(), key=lambda x: x[1], reverse=True)[:20]
        
        stats = {
            "metadata": self._metadata,
            "top_tokens": top_tokens,
            "average_tokens_per_document": self._metadata["token_count"] / self._metadata["document_count"] if self._metadata["document_count"] > 0 else 0,
            "unique_tokens": len(token_frequency),
            "index_size_kb": os.path.getsize(self.index_file) / 1024 if os.path.exists(self.index_file) else 0
        }
        
        return stats

def main():
    """主函数 - 用于演示和测试搜索索引优化器"""
    # 创建搜索索引优化器实例
    index_optimizer = SearchIndexOptimizer()
    
    # 构建索引
    index_optimizer.build_index(force_rebuild=True)
    
    # 优化索引
    index_optimizer.optimize_index()
    
    # 执行搜索测试
    test_queries = ["安装", "API", "搜索", "配置", "示例"]
    
    for query in test_queries:
        print(f"\n搜索查询: '{query}'")
        results = index_optimizer.search(query, limit=3)
        
        if results:
            print(f"找到 {len(results)} 个结果:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title']} (得分: {result['score']:.4f})")
                print(f"   路径: {result['path']}")
                print(f"   摘要: {result['snippet']}")
                print()
        else:
            print("未找到相关结果")
        
        # 测试搜索建议
        suggestions = index_optimizer.get_search_suggestions(query[:2], limit=3)
        if suggestions:
            print(f"搜索建议: {suggestions}")
    
    # 导出索引统计
    stats = index_optimizer.export_index_stats()
    print("\n索引统计信息:")
    print(f"文档数量: {stats['metadata']['document_count']}")
    print(f"总词语数: {stats['metadata']['token_count']}")
    print(f"平均每文档词语数: {stats['average_tokens_per_document']:.2f}")
    print(f"唯一词语数: {stats['unique_tokens']}")
    print(f"索引文件大小: {stats['index_size_kb']:.2f} KB")
    print("\n最常见的20个词语:")
    for token, count in stats['top_tokens'][:10]:  # 只显示前10个
        print(f"  '{token}': {count} 次")

if __name__ == "__main__":
    main()