package tictac;

import static org.junit.Assert.*;
import org.junit.Test;

import tictac.Board;
import tictac.Board.Taken;

import java.util.ArrayList;
import java.util.List;


public class TicTacWinnerTest {

  private Board testBoard1 = new Board();

  private TicTacWinner winner = new TicTacWinner();

  @Test
  public void isWinningTripleTest1() {
    ArrayList<Taken> list = new ArrayList<Taken>();
    list.add(Taken.EMPTY);
    list.add(Taken.EMPTY);
    list.add(Taken.EMPTY);

    assertFalse(winner.isWinningTriple(list));
  }

  @Test
  public void isWinningTripleTest2() {
    ArrayList<Taken> list = new ArrayList<Taken>();
    list.add(Taken.PLAYERA);
    list.add(Taken.EMPTY);
    list.add(Taken.EMPTY);

    assertFalse(winner.isWinningTriple(list));
  }

  @Test
  public void isWinningTripleTest3() {
    ArrayList<Taken> list = new ArrayList<Taken>();
    list.add(Taken.PLAYERA);
    list.add(Taken.PLAYERA);
    list.add(Taken.PLAYERA);

    assertTrue(winner.isWinningTriple(list));
  }

  @Test
  public void isWinningTripleTest4() {
    ArrayList<Taken> list = new ArrayList<Taken>();
    list.add(Taken.PLAYERB);
    list.add(Taken.PLAYERB);
    list.add(Taken.PLAYERB);

    assertTrue(winner.isWinningTriple(list));
  }

  @Test
  public void isWinningTripleTest5() {
    ArrayList<Taken> list = new ArrayList<Taken>();
    list.add(Taken.PLAYERB);
    list.add(Taken.PLAYERB);
    list.add(Taken.EMPTY);

    assertFalse(winner.isWinningTriple(list));
  }

  @Test
  public void isWinningTripleTest6() {
    ArrayList<Taken> list = new ArrayList<Taken>();
    list.add(Taken.PLAYERA);
    list.add(Taken.EMPTY);
    list.add(Taken.PLAYERA);

    assertFalse(winner.isWinningTriple(list));
  }

}


