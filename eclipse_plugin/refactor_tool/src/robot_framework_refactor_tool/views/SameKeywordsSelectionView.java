package robot_framework_refactor_tool.views;


import org.eclipse.swt.widgets.Composite;
import org.eclipse.ui.part.*;
import org.python.core.PyList;

import helper.NewRefactorHelper;
import robot_framework_refactor_tool.handlers.WrapStepsAsANewKeywordHandler;

import org.eclipse.jface.viewers.*;
import org.eclipse.swt.graphics.Image;
import org.eclipse.jface.action.*;
import org.eclipse.ui.*;

import java.util.ArrayList;
import java.util.List;

import javax.inject.Inject;

public class SameKeywordsSelectionView extends ViewPart {
	private WrapStepsAsANewKeywordHandler wrapHandler;
	private Node root;
	public static final String ID = "robot_framework_refactor_tool.views.SampleView";

	@Inject IWorkbench workbench;

	private TreeViewer viewer;
	private Action selectAllAction;
	private Action submitAction;
	private IWorkbenchWindow window;
	private NewRefactorHelper helper;
	
	public void update(Node root, WrapStepsAsANewKeywordHandler wrapHandler, IWorkbenchWindow window, NewRefactorHelper helper) {
		this.wrapHandler = wrapHandler;
		this.root = root;
		this.window = window;
		this.helper = helper;
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
			IStructuredSelection selectedSameStepsBlocks = (IStructuredSelection)event.getSelection();
			PyList sameStepsBlock = (PyList)((Node)selectedSameStepsBlocks.getFirstElement()).getData();
			AddArgumentsForKeywordReplacingSameSteps presentSameStepsDialog = new AddArgumentsForKeywordReplacingSameSteps(this.window.getShell(), this.helper, sameStepsBlock);
			presentSameStepsDialog.open();
			
		});
		viewer.addSelectionChangedListener(event -> {
			List<Node> selections = viewer.getStructuredSelection().toList();
			boolean shouldBeEnable = false;
			for (Node selection:selections) {	
				if(selection.toString().indexOf(".txt") == -1 & selection.toString().indexOf(".robot") == -1){
					shouldBeEnable = false;
					break;
				}
				else {
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
						if(node.getClass() == SameStepsBlock.class) {						
							allNodes.add(node);
						}
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
				PyList selectedSameKeywordsBlocks = new PyList(selections);
				wrapHandler.afterChoosingReplacedSteps(selectedSameKeywordsBlocks);
				viewer.setInput(null);
				viewer.refresh();
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
