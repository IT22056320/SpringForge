package org.SpringForge.actions

import com.intellij.notification.Notification
import com.intellij.notification.NotificationType
import com.intellij.notification.Notifications
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.fileEditor.FileEditorManager
import com.intellij.openapi.vfs.VirtualFile
import org.SpringForge.parser.YamlParser
import org.SpringForge.ui.YamlPreviewDialog


class OpenInputYmlAction : AnAction("CodeGeneration: Open input.yml") {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val base = project.baseDir ?: return

        // find or create input.yml in project root
        val file: VirtualFile = base.findChild("input.yml") ?: run {
            // directly create the file in the project root
            base.createChildData(this, "input.yml")
        }

        FileEditorManager.getInstance(project).openFile(file, true)

        val text = String(file.contentsToByteArray())
        val result = YamlParser.parse(text)
        if (!result.isValid) {
            Notifications.Bus.notify(Notification("SpringForge", "YAML parse error", result.errorMessage ?: "Unknown", NotificationType.ERROR), project)
            return
        }

        // show preview dialog
        YamlPreviewDialog(project, result.data!!).show()
    }
}