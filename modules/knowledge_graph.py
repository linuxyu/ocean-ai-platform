class KnowledgeGraph:
    """知识图谱构建与演化模块"""

    def __init__(self, config):
        self.config = config
        self.graph = {
            "entities": {},
            "relationships": {}
        }

    def update_graph(self, entities, relations):
        """增量更新知识图谱"""
        # 合并新实体
        for entity in entities:
            entity_id = entity.get('id')
            if entity_id:
                # 更新或添加实体
                if entity_id in self.graph["entities"]:
                    self.graph["entities"][entity_id].update(entity)
                else:
                    self.graph["entities"][entity_id] = entity

        # 添加新关系
        for relation in relations:
            rel_id = f"{relation['source']}-{relation['type']}-{relation['target']}"
            self.graph["relationships"][rel_id] = relation

        return self.graph

    def extract_entities(self, data):
        """从数据中提取实体"""
        # 简化的实现 - 实际应包含NLP处理
        entities = []

        if 'vessel' in data:
            entities.append({
                "id": data['vessel']['id'],
                "type": "Vessel",
                "properties": {
                    "type": data['vessel'].get('type'),
                    "status": "active"
                }
            })

        if 'equipment' in data:
            entities.append({
                "id": data['equipment']['id'],
                "type": "Equipment",
                "properties": data['equipment']
            })

        return entities

    def extract_relations(self, data):
        """从数据中提取关系"""
        relations = []

        if 'vessel' in data and 'equipment' in data:
            relations.append({
                "source": data['vessel']['id'],
                "target": data['equipment']['id'],
                "type": "has_equipment"
            })

        return relations

    def process(self, data):
        """处理数据并更新知识图谱"""
        entities = self.extract_entities(data)
        relations = self.extract_relations(data)

        self.graph = self.update_graph(entities, relations)

        return {
            "knowledge_graph": self.graph,
            "changes": {
                "entities_added": len(entities),
                "relations_added": len(relations)
            }
        }