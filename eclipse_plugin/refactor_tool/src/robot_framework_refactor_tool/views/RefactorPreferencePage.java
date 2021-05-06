package robot_framework_refactor_tool.views;

import org.eclipse.core.runtime.preferences.InstanceScope;
import org.eclipse.jface.preference.DirectoryFieldEditor;
import org.eclipse.jface.preference.FieldEditorPreferencePage;
import org.eclipse.ui.IWorkbench;
import org.eclipse.ui.IWorkbenchPreferencePage;
import org.eclipse.ui.preferences.ScopedPreferenceStore;

public class RefactorPreferencePage extends FieldEditorPreferencePage implements IWorkbenchPreferencePage{
	public RefactorPreferencePage() {
		super(GRID);
	}
	@Override
	public void init(IWorkbench workbench) {
		setPreferenceStore(new ScopedPreferenceStore(InstanceScope.INSTANCE, "robot_framework_refactor_tool.preference"));
		setDescription("Robot Framework Refactor Tool preference page");
	}

	@Override
	protected void createFieldEditors() {
		addField(new DirectoryFieldEditor("PYTHON", "&Python site-packages location:", getFieldEditorParent()));
	}

}
