import java.io.IOException;
import java.net.Socket;
import java.util.Random;
import java.util.Scanner;

public class ClientProtocol{

    private Socket sucked;
    private Scanner sc;
    private Utils utils;
    private boolean finalitzat;
    private int id;
    
    public ClientProtocol(Socket socket) throws IOException{
        this.sucked = socket;
        this.utils = new Utils(this.sucked);
        this.sc = new Scanner(System.in);
        this.finalitzat = false;
    }

    public int sendHello() throws IOException{
        Random rand = new Random();

        this.id = (int) rand.nextInt(90000)+10000;
        String name = "";
        while(name.isEmpty()){
            System.out.println("Write the your name:");
            name = sc.nextLine();
        }
        System.out.println("Your ID that we generated: " + id);
        this.utils.writeHello(id, name);
        return 2;
        
    }

    public int receiveReadyAndSendPlay() throws IOException{
        int id;
        Byte bytes = this.utils.read_Byte();
        if(bytes != 2){

        }
        int ids = this.utils.read_Int();
        String id_aux = "";
        while(id_aux.isEmpty()){
            System.out.println("Write your ID that we given to you:");
            id_aux = sc.nextLine();
        }

        id = Integer.parseInt(id_aux);
        this.utils.writePlay(id);
        return 3;
    }

    public int receiveAdmitAndSendAction() throws IOException{
        Byte bytes = this.utils.read_Byte();
        boolean admited = false;
        if(bytes == 8){
            this.utils.read_Byte();
            String message = this.utils.convertToString();
            admited = false;
        }else{
            admited = this.utils.read_Boolean();
        }
        if(!admited){
            int id;
            String id_aux = "";
            while(id_aux.isEmpty()){
                System.out.println("Write your ID that we given to you:");
                id_aux = sc.nextLine();
            }

            id = Integer.parseInt(id_aux);
            this.utils.writePlay(id);
            return 3;
        }

        String actiontext = "";
        while(!isCorrect(actiontext)){
            System.out.println("What action do you want to do?");
            actiontext = sc.nextLine();
            if(!isCorrect(actiontext)){
                System.out.println("Incorrect Action");
            }
        }

        this.utils.writeAction(actiontext);
        this.finalitzat = false;
        return 4;
    }

    public int receiveResultandSendAction() throws IOException{
        while(!this.finalitzat){
            Byte bytes = this.utils.read_Byte();
            if(bytes == 8){
                this.utils.read_Byte();
                this.utils.convertToString();
            }else{
                StringBuilder actionBuilder = new StringBuilder();
                for(int i = 0; i < 5; i++){
                    char chars = this.utils.read_Char();
                    actionBuilder.append(chars);
                }
                String actionName = actionBuilder.toString();

                if(actionName.equals("ENDS0") || actionName.equals("ENDS1")){
                    if (actionName.equals("ENDS0")) {
                        System.out.println("Wins the Server");
                    }else{
                        System.out.println("You are the Winner!");
                    }

                    while(!finalitzat){
                        System.out.println("Vols tornar a jugar? (S/N)");
                        String action = sc.nextLine();
                        int utilsAction;
                        if(action.equals("S")){
                            utilsAction = utils.write_Estat(action);
                            this.finalitzat = true;
                            utils.writePlay(this.id);
                            utils.reiniciarBullets();
                            return utilsAction;
                        }else if(action.equals("N")){
                            utilsAction = utils.write_Estat(action);
                            this.finalitzat = true;
                            return utilsAction;
                        }else{
                            this.finalitzat = false;
                        }
                    }

                    return 5;
                }else{
                    System.out.println("Action returning: " + actionName);
                }
            }
            
            String actiontext = "";
            while(!isCorrect(actiontext)){
                System.out.println("What action do you want to do?");
                actiontext = sc.nextLine();
                if(!isCorrect(actiontext)){
                    System.out.println("Incorrect Action");
                }
            }

            this.utils.writeAction(actiontext);
        }
        
        return 5;
    }

    private boolean isCorrect(String text){
        
        if(text.equals("BLOCK")  || text.equals("CHARG") || text.equals("SHOOT" )){

            return true;
        }
        return false;
    }

    




}