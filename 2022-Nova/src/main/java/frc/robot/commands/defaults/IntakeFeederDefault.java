package frc.robot.commands.defaults;

import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.IntakeFeeder;

public class IntakeFeederDefault extends CommandBase {
  /** Creates a new FeederDefault. */
  private IntakeFeeder intakeFeeder;
  private double time;
  public IntakeFeederDefault(IntakeFeeder intakeFeeder) {
    this.intakeFeeder = intakeFeeder;
    addRequirements(intakeFeeder);
  }

  @Override
  public void initialize() {
    time = Timer.getFPGATimestamp();
  }

  @Override
  public void execute() {
    intakeFeeder.setIntakeUp();
    intakeFeeder.setIntakePercent(0);

    System.out.println("Feeder Default");

    if (!intakeFeeder.getBottomBeamBreak()) {
      if (Timer.getFPGATimestamp() - time >= 0.2) {
        intakeFeeder.setBallCount(2);
        intakeFeeder.setBeltFalcon(0);
        intakeFeeder.setLowerFalcon(0);
      } else {
        intakeFeeder.setBeltFalcon(0.2);
        intakeFeeder.setLowerFalcon(0.2);
      }
    }
  }

  @Override
  public void end(boolean interrupted) {}

  @Override
  public boolean isFinished() {
    return false;
  }
}
