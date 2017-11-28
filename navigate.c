/**
This is the pseudocode for our navigation logic. It will update regularly given the rover's current position.

*/

enum {NORTH = 0, WEST, SOUTH, EAST} DIRECTION;

DIRECTION facing = NORTH;
int curColumnPos;
int curRowPos;
//returns the amount of counterclockwise rotation to apply in degrees.
//TODO: update this to actually move the rover to the correct heading instead of only returns what it "should" do.
int leftRotationDegrees (DIRECTION current, DIRECTION next) {
	if(current == next) {
		return 0;
	}
	else if ((current + next) % 2) == 0) {
		return 180;
	}
	else if ((current == (next + 1) % 4) {
		return 90;
	}
	return 270;
}
//returns true if the sensor array reads all black
bool isHit() {
	return false; //TODO: update with sensor array readings
}

int navigate (int targetCol, int targetRow) {
	if (curColPos == targetCol) {
		if(curRowPos == targetRow) {
			return (isHit()) ? 1 : 0;
		}
		else if (curRowPos < targetRow) {
			//turn south
			leftRotationDegrees(facing, SOUTH); //this can be returned for debugging
			facing = SOUTH;
		}
		else {
			//turn north
			leftRotationDegrees(facing, NORTH); //this can be returned for debugging
			facing = NORTH;
		}
	}
	else {
		if (curColPos < targetCol) {
			//turn east
			leftRotationDegrees(facing, EAST); //this can be returned for debugging
			facing = EAST;
		}
		else {
			//turn west
			leftRotationDegrees(facing, WEST); //this can be returned for debugging
			facing = WEST;
		}
		
	}
	return 2;
}