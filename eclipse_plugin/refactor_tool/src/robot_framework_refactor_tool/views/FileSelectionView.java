package robot_framework_refactor_tool.views;


import org.eclipse.swt.widgets.Composite;
import org.eclipse.ui.part.*;


import org.eclipse.jface.viewers.*;
import org.eclipse.swt.graphics.Image;
import org.eclipse.jface.action.*;
import org.eclipse.ui.*;

import java.util.List;

import javax.inject.Inject;

import robot_framework_refactor_tool.handlers.MoveKeywordDefinedToAnotherFileHandler;
import robot_framework_refactor_tool.handlers.WrapStepsAsANewKeywordHandler;

public class FileSelectionView extends ViewPart {
	private WrapStepsAsANewKeywordHandler wrapHandler = null;
	private MoveKeywordDefinedToAnotherFileHandler moveHandler = null;
	public static final String ID = "robot_framework_refactor_tool.views.SampleView";

	@Inject IWorkbench workbench;

	private TreeViewer viewer;
	private Action submitAction;
	
	public void update(Node root, WrapStepsAsANewKeywordHandler wrapHandler) {
		this.wrapHandler = wrapHandler;
		this.viewer.setInput(root);
		this.viewer.refresh();
	}
	
	public void update(Node root, MoveKeywordDefinedToAnotherFileHandler moveHandler) {
		this.moveHandler = moveHandler;
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
		viewer.addSelectionChangedListener(event -> {
			boolean shouldBeEnable = false;
			List<Node> selections = viewer.getStructuredSelection().toList();
			if(selections.size()==1) {
				if(selections.get(0).toString().indexOf(".txt") != -1 | selections.get(0).toString().indexOf(".robot") != -1){
					shouldBeEnable = true;
				}
			}
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
		manager.add(submitAction);
	}

	private void makeActions() {
		submitAction = new Action() {
			public void run() {
				List<Node> selections = viewer.getStructuredSelection().toList();
				String selectionPath = selections.get(0).toString();
				viewer.setInput(null);
				viewer.refresh();
				if (wrapHandler!=null) {
					wrapHandler.afterChoosingFileToCreateKeyword(selectionPath);
					wrapHandler = null;
				}
				else {
					moveHandler.afterChoosingFileToInsertMovedKeyword(selectionPath);
					moveHandler = null;
				}
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
