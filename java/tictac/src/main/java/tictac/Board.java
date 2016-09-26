package tictac;

import java.util.ArrayList;
import java.util.List;

public class Board {
  public enum Taken {EMPTY, PLAYERA, PLAYERB}
  private ArrayList<ArrayList<Taken> > board;

  public Board() {
    // creates an empty board
    board = new ArrayList<ArrayList<Taken> >();
    for (int i = 0; i < 3; i++) {
      board.add(new ArrayList<Taken>());
      for (int j = 0; j < 3; j++) {
        board.get(i).add(Taken.EMPTY);
      }
    }

  }
}
