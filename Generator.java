// 0123456789ABCDEF

import java.awt.Color;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Random;
import java.util.Stack;

import javax.imageio.ImageIO;

// 320 lines of code (+printBoxMaze())

public class Generator {

	public static void main(String[] args) {

		boolean printMaze = true;
		int width = 3;
		int height = 3;
//		int spacing = 4;
		int startX = width - 1;
		int startY = height - 1;
		int endX = 0;
		int endY = 0;
		long startTime = System.currentTimeMillis();

		try {
			width = Integer.parseInt(args[0]);
		} catch (Exception e) {}

		try {
			height = Integer.parseInt(args[1]);
		} catch (Exception e) {}

		try {
//			spacing = Integer.parseInt(args[2]);
		} catch (Exception e) {}

//		System.out.println("Generating " + width + "x" + height + " maze, please wait...");

		Maze maze = new Maze(width, height, startX, startY);
		int solutionLength = 0;

		// the path
		Stack<Coordinate> path = new Stack<Coordinate>();
		path.push(maze.coordinate());
		Stack<Coordinate> solution = new Stack<Coordinate>();
		boolean solved = false;
		int emptyCells = maze.emptyCells();
		int step = 0;

		while(!path.isEmpty()) {

			step++;

			// visit new cell
			if(maze.unvisitedNeighbours()) {

				maze.randomMove();
				if(maze.unvisitedNeighbours()) {
					path.push(maze.coordinate());
				}
				emptyCells--;

				// dead end, go back until unvisited neighbors exist
			} else {

				Coordinate move = path.pop();
				maze.move(move);
				if(maze.unvisitedNeighbours()) {
					path.push(move);
				}
			}

			// the solution
			if(maze.coordinate().equals(endX, endY) && !solved) {
				// Objects use '=' symbolically
				solution.addAll(path);
				solutionLength = path.size();
				solved = true;
			}

			// exit loop when maze is finished
			if(emptyCells == 0) {
				break;
			}
		}

//		System.out.println("Generating: " + (System.currentTimeMillis() - startTime) + "ms");
//		System.out.println("Length of solution: " + solutionLength);
//		System.out.println("Number of generations: " + step);
		
		// printing maze on command line
		if(printMaze) {
			startTime = System.currentTimeMillis();
//			maze.printMaze();
			maze.printBoxMaze();
//			System.out.println("Printing maze: " + (System.currentTimeMillis() - startTime) + "ms");
		}

		// drawing the maze onto a PNG file
/*		startTime = System.currentTimeMillis();
		System.out.println("Drawing maze onto a PNG file, please wait...");
		maze.drawMaze(spacing, startX, startY, endX, endY, solution);
		System.out.println("Drawing maze: " + (System.currentTimeMillis() - startTime) + "ms");
		System.out.println("Done.");
*/	}
}

class Maze {
	
	private boolean[] cells;
	private boolean[] walls;
	private Coordinate coordinate;
	private int width;
	private int height;

	public static final boolean UNVISITED = false;
	public static final boolean VISITED = true;

	Random random = new Random();

	public Maze(int width, int height, int x, int y) {
		this.cells = new boolean[width * height];
		this.walls = new boolean[(width - 1) * height + width * (height - 1)];
		this.coordinate = new Coordinate(x, y);
		this.width = width;
		this.height = height;

		// initializing arrays
		for(int i = 0; i < cells.length; i++) {
			cells[i] = UNVISITED;
		}
		for(int i = 0; i < walls.length; i++) {
			walls[i] = true;
		}
		
		this.cells[y * width + x] = VISITED;
	}

	public Coordinate coordinate() {
		return new Coordinate(this.coordinate);
	}
	
	public int emptyCells() {
		int emptyCells = this.cells.length;
		for(int i = 0; i < this.cells.length; i++) {
			if(cells[i]) {
				emptyCells--;
			}
		}
		return emptyCells;
	}
	
	public void move(Coordinate coordinate) {
		this.coordinate = new Coordinate(coordinate);
	}

	public void move(Direction direction) {
			
			// up
		if(direction == Direction.UP) {

			// move up
			if(this.coordinate.y() > 0) {
				this.coordinate.move(Direction.UP);
			} else {
				throw new RuntimeException();
			}

			// remove wall between new and old cell
			this.walls[(this.height * (this.width - 1)) + (this.coordinate.y() * this.width + this.coordinate.x())] = false;

			// right
		} else if(direction == Direction.RIGHT) {

			// move right
			if(this.coordinate.x() < this.width - 1) {
				this.coordinate.move(Direction.RIGHT);
			} else {
				throw new RuntimeException();
			}

			// remove wall between new and old cell
			this.walls[this.coordinate.y() * (this.width - 1) + this.coordinate.x() - 1] = false;

			// down
		} else if(direction == Direction.DOWN) {

			// move down
			if(this.coordinate.y() < this.height - 1) {
				this.coordinate.move(Direction.DOWN);
			} else {
				throw new RuntimeException();
			}

			// remove wall between new and old cell
			this.walls[(this.height * (this.width - 1)) + ((this.coordinate.y() - 1) * this.width + this.coordinate.x())] = false;

			// left
		} else if(direction == Direction.LEFT) {

			// move left
			if(this.coordinate.x() > 0) {
				this.coordinate.move(Direction.LEFT);
			} else {
				throw new RuntimeException();
			}

			// remove wall between new and old cell
			this.walls[this.coordinate.y() * (this.width - 1) + this.coordinate.x()] = false;
		}

		this.cells[this.coordinate.y() * this.width + this.coordinate.x()] = VISITED;
	}

	public boolean unvisitedNeighbours() {
		// above
		if(this.coordinate.y() > 0 && !isVisited(this.coordinate.x(), this.coordinate.y() - 1)) {
			return true;
		}

		// right
		if(this.coordinate.x() < this.width - 1 && !isVisited(this.coordinate.x() + 1, this.coordinate.y())) {
			return true;
		}

		// below
		if(this.coordinate.y() < this.height - 1 && !isVisited(this.coordinate.x(), this.coordinate.y() + 1)) {
			return true;
		}

		// left
		if(this.coordinate.x() > 0 && !isVisited(this.coordinate.x() - 1, this.coordinate.y())) {
			return true;
		}

		return false;
	}
	
	public void randomMove() {
		int validDirections = 0;
		Direction[] directions = new Direction[4];
		
		// up
		if(this.coordinate.y() > 0 && !isVisited(this.coordinate.x(), this.coordinate.y() - 1)) {
			directions[validDirections] = Direction.UP;
			validDirections++;
		}

		// right
		if(this.coordinate.x() < this.width - 1 && !isVisited(this.coordinate.x() + 1, this.coordinate.y())) {
			directions[validDirections] = Direction.RIGHT;
			validDirections++;
		}

		// down
		if(this.coordinate.y() < this.height - 1 && !isVisited(this.coordinate.x(), this.coordinate.y() + 1)) {
			directions[validDirections] = Direction.DOWN;
			validDirections++;
		}

		// left
		if(this.coordinate.x() > 0 && !isVisited(this.coordinate.x() - 1, this.coordinate.y())) {
			directions[validDirections] = Direction.LEFT;
			validDirections++;
		}
		Direction move = directions[random.nextInt(validDirections)];
		this.move(move);
	}

	public boolean isVisited(int x, int y) {
		return this.cells[y * this.width + x];
	}

// 0123456789ABCDEF

	public void printBoxMaze() {
	
	    boolean[] verticals = new boolean[this.width+1];
		for(int x = 0; x < this.width+1; x++) {
		    verticals[x] = false;
		}

        printBlock(6);
		for(int x = 0; x < this.width - 1; x++) {
		    int block = 10; // up=1 right=2 down=4 left=8

		    if(this.walls[x]) {
		        block += 4;
            	verticals[x] = true;
		    }
 			printBlock(block);
 		}
 		printBlock(12);
 		System.out.println();
	
		for(int y = 0; y < this.height; y++) {

//		    System.out.println(y);
    	    boolean horizontal = false;
 //   	    verticals[0] = true;
			for(int x = 0; x < this.width; x++) {
			    int block = 0; // up=1 right=2 down=4 left=8
    		    if(x == 0 || verticals[x-1]) {
	    	        block += 1;
                }
                if(horizontal) {
                    block += 8;
                }
    			if((x == 0 || this.walls[(y + 1) * (this.width - 1) + x - 1]) && y < this.height - 1) {
                    block += 4;
                    if(x > 0) {
    	    			verticals[x-1] = true;
    	    		}
		    	} else if(x > 0) {
                   verticals[x-1] = false;
			    }
		    	if(y == this.height -1 || this.walls[(this.height * (this.width - 1)) + (y * this.width + x)]) {
			        block += 2;
	    		    horizontal = true;
    			} else {
		    	    horizontal = false;
			    }
			    printBlock(block);
			}
		    int block = 1; // up=1 right=2 down=4 left=8
            if(horizontal) {
                block += 8;
            }
            if(y < this.height - 1) {
                block += 4;
            }
            printBlock(block);
            
		    System.out.println();
		}
	}

    public void printBlock(int block) {
  		if(block < 10) {
		    System.out.print(block);
		} else if(block == 10) {
		    System.out.print("A");
		} else if(block == 11) {
		    System.out.print("B");
		} else if(block == 12) {
		    System.out.print("C");
		} else if(block == 13) {
		    System.out.print("D");
		} else if(block == 14) {
		    System.out.print("E");
		} else if(block == 15) {
		    System.out.print("F");
	    }
	}

	public void printMaze() {

		// top line
		System.out.print("\t");
		for(int x = 0; x < this.width; x++) {
			System.out.print("+---");
		}
		System.out.println("+");

		// main maze
		for(int y = 0; y < this.height - 1; y++) {
			// vertical walls
			System.out.print(y + "\t|");
			for(int x = 0; x < this.width - 1; x++) {
				if(this.walls[y * (this.width - 1) + x]) {
					System.out.print("   |");
				} else {
					System.out.print("    ");
				}
			}
			
			System.out.println("   |");
			
			// horizontal walls
			System.out.print("\t");
			for(int x = 0; x < this.width; x++) {
				if(walls[(this.height * (this.width - 1)) + (y * this.width + x)]) {
					System.out.print("+---");
				} else {
					System.out.print("+   ");
				}
			}
			System.out.println("+");
		}

		// vertical walls
		System.out.print((height - 1) + "\t|");
		for(int x = 0; x < this.width - 1; x++) {
			if(walls[(this.height - 1) * (this.width - 1) + x]) {
				System.out.print("   |");
			} else {
				System.out.print("    ");
			}
		}
		
		System.out.println("   |");

		// bottom line
		System.out.print("\t");
		for(int x = 0; x < this.width; x++) {
			System.out.print("+---");
		}
		System.out.println("+");
	}

	public void drawMaze(int spacing, int startX, int startY, int endX, int endY, Stack<Coordinate> solution) {

		BufferedImage image = new BufferedImage(this.width * spacing + 1, this.height * spacing + 1, BufferedImage.TYPE_INT_RGB);

		Graphics graphics = image.getGraphics();
		graphics.setColor(Color.WHITE);
		graphics.fillRect(0, 0, this.width * spacing + 1, this.height * spacing + 1);

		// start and end
		graphics.setColor(Color.RED);
		graphics.fillOval(startX * spacing, startY * spacing, spacing, spacing);
		graphics.fillOval(endX * spacing, endY * spacing, spacing, spacing);

		// bounds
		graphics.setColor(Color.BLACK);
		graphics.drawLine(0, 0, this.width * spacing, 0);
		graphics.drawLine(0, 0, 0, this.height * spacing);
		graphics.drawLine(0, this.height * spacing, this.width * spacing, this.height * spacing);
		graphics.drawLine(this.width * spacing, 0, this.width * spacing, this.height * spacing);

		// vertical lines
		for(int y = 0; y < this.height; y++) {
			for(int x = 0; x < this.width - 1; x++) {
				if(this.walls[y * (this.width - 1) + x]) {
					graphics.drawLine(x * spacing + spacing, y * spacing, x * spacing + spacing, y * spacing + spacing);
				}
			}
		}

		// horizontal lines
		for(int y = 0; y < this.height - 1; y++) {
			for(int x = 0; x < this.width; x++) {
				if(this.walls[y * this.width + x + this.height * (this.width - 1)]) {
					graphics.drawLine(x * spacing, y * spacing + spacing, x * spacing + spacing, y * spacing + spacing);
				}
			}
		}

		System.out.println("Writing maze...");

		// write image as PNG onto file
		try {
			ImageIO.write(image, "png", new File("maze.png"));
		} catch (IOException e) {
			e.printStackTrace();
		}


		// solution
		graphics.setColor(Color.RED);
		Coordinate previousCoordinate = solution.pop();
		Coordinate currentCoordinate;
		while(!solution.isEmpty()) {
			currentCoordinate = solution.pop();
			graphics.drawLine(previousCoordinate.x() * spacing + spacing / 2, previousCoordinate.y() * spacing + spacing / 2,
					currentCoordinate.x() * spacing + spacing / 2, currentCoordinate.y() * spacing + spacing / 2);
			previousCoordinate = currentCoordinate;
		}

		System.out.println("Writing solution...");

		// write image as PNG onto file
		try {
			ImageIO.write(image, "png", new File("mazeSolution.png"));
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
}

class Coordinate {
	
	private int x;
	private int y;
	
	public Coordinate(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public Coordinate(Coordinate anotherCoordinate) {
		this.x = anotherCoordinate.x();
		this.y = anotherCoordinate.y();
	}
	
	public int x() {
		return this.x;
	}
	
	public int y() {
		return this.y;
	}
	
	public void move(Direction direction) {
		if(direction == Direction.UP) {
			this.y--;
		}
		
		if(direction == Direction.RIGHT) {
			this.x++;
		}
		
		if(direction == Direction.DOWN) {
			this.y++;
		}
		
		if(direction == Direction.LEFT) {
			this.x--;
		}
	}
	
	public boolean equals(int x, int y) {
		return this.x == x && this.y == y;
	}
	
	public int hashCode() {
		return this.y * 256 + this.x;
	}

}

enum Direction {
	UP, RIGHT, DOWN, LEFT;
}
