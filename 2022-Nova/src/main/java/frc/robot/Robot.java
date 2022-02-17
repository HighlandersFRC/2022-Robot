package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import frc.robot.commands.FaceTarget;
import frc.robot.commands.ClimbRobot;
import frc.robot.commands.ContinuousAccelerationInterpolation;
import frc.robot.commands.EjectBalls;
import frc.robot.commands.FireBalls;
import frc.robot.commands.IntakeBalls;
import frc.robot.commands.RaiseClimber;
import frc.robot.commands.SetHoodPosition;
import frc.robot.commands.SpinShooter;
import frc.robot.commands.autos.ThreeBallAuto;
import frc.robot.subsystems.Climber;
import frc.robot.subsystems.Drive;
import frc.robot.subsystems.Feeder;
import frc.robot.subsystems.Intake;
import frc.robot.subsystems.LinearActuator;
import frc.robot.subsystems.MqttPublish;
import frc.robot.subsystems.MqttSubscribe;
import frc.robot.subsystems.Peripherals;
import frc.robot.subsystems.Shooter;
import frc.robot.tools.PneumaticsControl;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.json.JSONArray;
import org.json.JSONTokener;

public class Robot extends TimedRobot {
  private Command m_autonomousCommand;

  private RobotContainer m_robotContainer;
  File f;
  BufferedWriter bw;
  FileWriter fw;
  double startTime;

  File pathingFile;
  String pathString;

  JSONArray pathJSON;

  ContinuousAccelerationInterpolation testPath;

  
  
  private final Shooter shooter = new Shooter();
  private final LinearActuator linearActuator = new LinearActuator();
  private final Feeder feeder = new Feeder();
  private final PneumaticsControl pneumatics = new PneumaticsControl();
  private final Intake intake = new Intake(pneumatics);
  private final Climber climber = new Climber(pneumatics);

  private final String subCameraTopic = "/sensors/camera";
  private final String pubCameraTopic = "/robot/camera";

  private MqttPublish publish = new MqttPublish();
  private MqttSubscribe subscribe = new MqttSubscribe();

  private final Peripherals peripherals = new Peripherals(subscribe);

  private final Drive drive = new Drive(peripherals);

  private ThreeBallAuto threeBallAuto = new ThreeBallAuto(drive, intake, feeder, shooter, linearActuator);


  /**
   * This function is run when the robot is first started up and should be used
   * for any initialization code.
   */
  @Override
  public void robotInit() {
    // System.out.println("###########");
    drive.init();
    peripherals.init();
    intake.init();
    shooter.init();
    linearActuator.init();
    feeder.init();
    climber.init();

    // publish.publish(pubCameraTopic);
    subscribe.subscribe(subCameraTopic);
    m_robotContainer = new RobotContainer();

    try {
      pathingFile = new File("/home/lvuser/deploy/TurnTest.json");
      FileReader scanner = new FileReader(pathingFile);
      pathJSON = new JSONArray(new JSONTokener(scanner));
      System.out.println(pathJSON);
    }
    catch(Exception e) {
      System.out.println("ERROR WITH PATH FILE " + e);
    }
  }

  @Override
  public void robotPeriodic() {
    // SmartDashboard.putNumber("Navx Value", peripherals.getNavxAngle());
    // System.out.println("^^^^^^^^^^^^^^^^^^^ " + drive.getOdometryAngle());
    CommandScheduler.getInstance().run();
    // System.out.println(">>>>>>>>>>>>>>>>>>> " + drive.getOdometryAngle());
    // System.out.println((peripherals.getRawNavxAngle()));
    }
  

  /** This function is called once each time the robot enters Disabled mode. */
  @Override
  public void disabledInit() {
    try {
      if(bw != null){ 
        bw.close();
      }
      if(fw != null){
        fw.close();
      }
     
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    
  }

  @Override
  public void disabledPeriodic() {}

  @Override
  public void autonomousInit() {
    System.out.println(pathJSON);
    drive.autoInit(pathJSON);
    // peripherals.init();
    // testPath = new ContinuousAccelerationInterpolation(drive, pathJSON);
    // testPath.schedule();
    threeBallAuto.schedule();
  }

  /** This function is called periodically during autonomous. */
  @Override
  public void autonomousPeriodic() {}

  @Override
  public void teleopInit() {
    startTime = Timer.getFPGATimestamp();
    // try{
    //   f = new File("/home/lvuser/Navx/NavxValues" +  (int) startTime + ".csv");
    //   if(!f.exists()){
    //     f.createNewFile();  
    //   }
    //   fw = new FileWriter(f);
    //   bw = new BufferedWriter(fw);
    //   bw.write("started collecting \n" );
      
      
    //   }
    //   catch (Exception e){
    //     e.printStackTrace();
    //   }

    if (m_autonomousCommand != null) {
      m_autonomousCommand.cancel();
    }

    // OI.driverA.whenPressed(new DriveForward(drive, 2, true));
    // OI.driverB.whenPressed(new DriveForward(drive, 2, false));

    OI.driverRT.whileHeld(new IntakeBalls(intake));
    OI.driverLT.whileHeld(new EjectBalls(feeder, 0.4, -1));
    // OI.driverB.whileHeld(new IntakeUp(intake));

    // OI.driverA.whileHeld(new SetHoodPosition(linearActuator, 0.2));
    // OI.driverB.whileHeld(new SetHoodPosition(linearActuator, 0.4));
    // OI.driverY.whileHeld(new SetHoodPosition(linearActuator, 0.6));

    OI.driverA.whenPressed(new FireBalls(intake, feeder, shooter, linearActuator, 0, 1500));
    OI.driverB.whenPressed(new FireBalls(intake, feeder, shooter, linearActuator, 0.3, 3150));
    OI.driverX.whenPressed(new FireBalls(intake, feeder, shooter, linearActuator, 0.7, 2500));

    OI.driverY.whenPressed(new FaceTarget(drive, Math.PI / 4));
  

    // OI.driverB.whileHeld(new SpinShooter(shooter, 0.5));

    OI.driverX.whenReleased(new SetHoodPosition(linearActuator, 0));
    OI.driverX.whenReleased(new EjectBalls(feeder, 0, -1));
    OI.driverX.whenReleased(new SpinShooter(shooter, 0));

    OI.operatorX.whileHeld(new RaiseClimber(climber));
    OI.operatorB.whileHeld(new ClimbRobot(climber));
  }

  /** This function is called periodically during operator control. */
  @Override
  public void teleopPeriodic() {
    //System.out.println(peripherals.getNavxAngle());
    // System.out.println(pathJSON.toString());
    //    try{
    //   bw.write(Timer.getFPGATimestamp() - startTime + ",");
    //   bw.write( peripherals.getNavxYaw() + ",");
    //   bw.write( peripherals.getNavxRoll() + ",");
    //   bw.write( peripherals.getNavxPitch() + "\n");
    // } catch (Exception e){
    //   e.printStackTrace();
    // }
    SmartDashboard.putNumber("Controller Y", OI.getDriverLeftY());
    SmartDashboard.putNumber("Controller X", OI.getDriverLeftX());
    SmartDashboard.putNumber("RPM", shooter.getShooterRPM());
  }

  @Override
  public void testInit() {
    OI.driverRT.whileHeld(new IntakeBalls(intake));
    // Cancels all running commands at the start of test mode.
    CommandScheduler.getInstance().cancelAll();
  }

  /** This function is called periodically during test mode. */
  @Override
  public void testPeriodic() {}
}
