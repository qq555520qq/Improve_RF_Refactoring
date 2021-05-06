package robot_framework_refactor_tool.views;


import org.eclipse.swt.widgets.Composite;
import org.eclipse.ui.part.*;

import org.eclipse.jface.viewers.*;
import org.eclipse.jface.window.Window;
import org.eclipse.swt.graphics.Image;
import org.eclipse.jface.action.*;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.ui.*;

import java.util.ArrayList;
import java.util.List;

import javax.inject.Inject;

public class ShowReferencesView extends ViewPart {
	private Node root;
	private RenameAction renameAction;
	private ModifyAction modifyAcyion;
	public static final String ID = "robot_framework_refactor_tool.views.SampleView";

	@Inject IWorkbench workbench;

	private TreeViewer viewer;
	private Action selectAllAction;
	private Action submitAction;
	
	public void update(Node root, RenameAction renameAction, ModifyAction modifyAction) {
		this.root = root;
		this.renameAction = renameAction;
		this.modifyAcyion = modifyAction;
		this.viewer.setInput(root);
		this.viewer.refresh();
	}
	
	class ViewLabelProvider implements ILabelProvider {
		@Override
		public Image getImage(Object obj) {
			return workbench.getSharedImages().getImage(ISharedImages.IMG_OBJ_ELEMENT);
		}
		@Override
		public void addListener(ILabelProviderListener listener) {
			// TODO Auto-generated method stub
			
		}
		@Override
		public void dispose() {
			// TODO Auto-generated method stub
			
		}
		@Override
		public boolean isLabelProperty(Object element, String property) {
			// TODO Auto-generated method stub
			return false;
		}
		@Override
		public void removeListener(ILabelProviderListener listener) {
			// TODO Auto-generated method stub
			
		}
		@Override
		public String getText(Object element) {
			Node node = (Node)element;
			return node.toString();
		}
	}
		
	class TreeContentProvider implements ITreeContentProvider{

		@Override
		public Object[] getElements(Object inputElement) {
			Node data = (Node)inputElement;
			return data.getChildren().toArray();
		}

		@Override
		public Object[] getChildren(Object parentElement) {
			Node data = (Node)parentElement;
			return data.getChildren().toArray();
		}

		@Override
		public Object getParent(Object element) {
			Node reference = (Node)element;
			return reference.getParent();
		}

		@Override
		public boolean hasChildren(Object element) {
			Node node = (Node)element;
			return node.hasChildren();
		}
		
	}

	@Override
	public void createPartControl(Composite parent) {
		viewer = new TreeViewer(parent);
		viewer.setContentProvider(new TreeContentProvider());
		viewer.setLabelProvider(new ViewLabelProvider());
		viewer.addDoubleClickListener(event->{
			IStructuredSelection sel = (IStructuredSelection)event.getSelection();
			Node reference = (Node)sel.getFirstElement();
			if (reference instanceof Step) {
				Step step = (Step)reference;
				InputDialog referenceDialog = new InputDialog(getViewSite().getShell(), "Reference Preview", "Modify the reference", reference.toString(), null);
				if(referenceDialog.open()==Window.OK && modifyAcyion!=null) {
					modifyAcyion.modify(step, referenceDialog.getValue());
					viewer.setInput(root);
				}
			}
			
			
		});
		viewer.addSelectionChangedListener(event -> {
			List<Node> selections = viewer.getStructuredSelection().toList();
			boolean shouldBeEnable = selections.size()>0;
			submitAction.setEnabled(shouldBeEnable);
		});
		workbench.getHelpSystem().setHelp(viewer.getControl(), "robot_framework_refactor_tool.viewer");
		getSite().setSelectionProvider(viewer);
		makeActions();
		contributeToActionBars();
	}

	private void contributeToActionBars() {
		IActionBars bars = getViewSite().getActionBars();
		fillLocalToolBar(bars.getToolBarManager());
	}

	private void fillLocalToolBar(IToolBarManager manager) {
		manager.add(selectAllAction);
		manager.add(submitAction);
	}

	private void makeActions() {
		selectAllAction = new Action() {
			public void run() {
				viewer.expandAll();
				List<Node> allNodes = new ArrayList<Node>();
				root.accept(new NodeVisitor(){
					@Override
					public boolean visit(Node node) {
						allNodes.add(node);
						return true;
					}
					
				});
				viewer.setSelection(new StructuredSelection(allNodes), true);
			}
		};
		selectAllAction.setText("Select All");
		submitAction = new Action() {
			public void run() {
				List<Node> selections = viewer.getStructuredSelection().toList();
				renameAction.rename(selections);
			}
		};
		this.submitAction.setText("Submit");
		submitAction.setEnabled(false);
	}

	@Override
	public void setFocus() {
		viewer.getControl().setFocus();
	}
	
}
