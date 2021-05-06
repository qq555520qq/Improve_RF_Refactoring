package robot_framework_refactor_tool.views;

import java.util.ArrayList;
import java.util.List;
import org.python.core.PyObject;

public class Node{
	private List<Node> children;
	private Node parent;
	private Object data;
	public Node(Object data) {
		this.data = data;
		this.children = new ArrayList<>();
	}
	
	public Node() {
		this.children = new ArrayList<>();
	}
	
	public void addChild(Node node){
		this.children.add(node);
		node.setParent(this);
	}
	
	public List<Node> getChildren(){
		return this.children;
	}
	
	public boolean hasChildren(){
		return !this.children.isEmpty();
	}
	
	public void setParent(Node parent) {
		this.parent = parent;
	}
	
	public Node getParent() {
		return this.parent;
	}
	
	public Object getData() {
		return this.data;
	}
		
	public void accept(NodeVisitor visitor) {
		boolean shouldContinue = visitor.visit(this);
		if(shouldContinue)
			for(Node child:children)
				child.accept(visitor);
	}
}

class TestDataFile extends Node{
	public TestDataFile(Object data) {
		super(data);
	}
	@Override
	public String toString() {
		PyObject data = (PyObject)this.getData();
		return data.__getattr__("source").toString();
	}
}
