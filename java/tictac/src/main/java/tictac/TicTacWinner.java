package tictac;

import java.util.ArrayList;
import java.util.List;
import tictac.Board.*;
import tictac.Board.Taken.*;



public class TicTacWinner {

  public boolean isWinningTriple(ArrayList<Taken> line) {
    if (line.size() != 3 || line.get(0) == Taken.EMPTY) return false;
    return (line.get(0) == line.get(1) && line.get(0) == line.get(2));
  }

}