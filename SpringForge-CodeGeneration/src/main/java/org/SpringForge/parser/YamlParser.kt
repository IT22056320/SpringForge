package org.SpringForge.parser

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory
import com.fasterxml.jackson.module.kotlin.KotlinModule
import com.fasterxml.jackson.module.kotlin.readValue

data class InputModel(
    val projectName: String = "",
    val packageRoot: String = "com.example",
    val architecture: String? = null,
    val entities: List<EntitySpec> = emptyList()
)
data class EntitySpec(val name: String = "", val fields: List<FieldSpec> = emptyList())
data class FieldSpec(val name: String = "", val type: String = "String", val annotations: List<String> = emptyList())

data class ParseResult(val isValid: Boolean, val errorMessage: String? = null, val data: InputModel? = null)

object YamlParser {
    private val mapper = ObjectMapper(YAMLFactory()).registerModule(KotlinModule())

    fun parse(text: String): ParseResult {
        return try {
            val model: InputModel = mapper.readValue(text)
            if (model.entities.isEmpty()) {
                ParseResult(false, "No entities declared in input.yml", null)
            } else ParseResult(true, null, model)
        } catch (ex: Exception) {
            ParseResult(false, "YAML parse error: ${ex.message}", null)
        }
    }
}
