package org.SpringForge.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.Messages
import org.SpringForge.parser.InputModel

class YamlPreviewDialog(private val project: Project, private val model: InputModel) {
    fun show() {
        val sb = StringBuilder()
        sb.append("Project: ${model.projectName}\n")
        sb.append("Package root: ${model.packageRoot}\n")
        sb.append("Architecture: ${model.architecture}\n")
        sb.append("Entities:\n")
        model.entities.forEach { e ->
            sb.append(" - ${e.name} (${e.fields.size} fields)\n")
        }
        Messages.showInfoMessage(project, sb.toString(), "Parsed input.yml")
    }
}
