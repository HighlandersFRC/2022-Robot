// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands.autos;

import java.io.File;
import java.io.FileReader;

import org.json.JSONArray;
import org.json.JSONTokener;

import edu.wpi.first.wpilibj2.command.ParallelRaceGroup;
import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import edu.wpi.first.wpilibj2.command.WaitCommand;
import frc.robot.commands.ContinuousAccelerationInterpolation;
import frc.robot.commands.FireBalls;
import frc.robot.commands.IntakeBalls;
import frc.robot.subsystems.Drive;
import frc.robot.subsystems.Feeder;
import frc.robot.subsystems.Intake;
import frc.robot.subsystems.LinearActuator;
import frc.robot.subsystems.Shooter;

// NOTE:  Consider using this command inline, rather than writing a subclass.  For more
// information, see:
// https://docs.wpilib.org/en/stable/docs/software/commandbased/convenience-features.html
public class FiveBallAuto extends SequentialCommandGroup {
  /** Creates a new FiveBallAuto. */
  private File pathingFile;
  private File pathingFile2;
  private JSONArray pathJSON;
  private JSONArray pathJSON2;

  public FiveBallAuto(Drive drive, Intake intake, Feeder feeder, Shooter shooter, LinearActuator linearActuator) {
    try {
      pathingFile = new File("/home/lvuser/deploy/Adj3Ball.json");
      FileReader scanner = new FileReader(pathingFile);
      pathJSON = new JSONArray(new JSONTokener(scanner));

      pathingFile2 = new File("/home/lvuser/deploy/5BallAutoPart2.json");
      FileReader scanner2 = new FileReader(pathingFile2);
      pathJSON2 = new JSONArray(new JSONTokener(scanner2));
    }
    catch(Exception e) {
      System.out.println("ERROR WITH PATH FILE " + e);
    }
    // Add your commands in the addCommands() call, e.g.
    // addCommands(new FooCommand(), new BarCommand());
    addRequirements(drive, intake);
    addCommands(new FireBalls(intake, feeder, shooter, linearActuator, 0.5, 2300), new ParallelRaceGroup(new ContinuousAccelerationInterpolation(drive, pathJSON, false), new IntakeBalls(intake)), new FireBalls(intake, feeder, shooter, linearActuator, 0.5, 2600), new ParallelRaceGroup(new ContinuousAccelerationInterpolation(drive, pathJSON2, false), new IntakeBalls(intake)));
  }
}

