import java.io.IOException;
import java.net.Socket;

public class GameProtocol{

    private Socket sucked;
    private int id;
    private boolean admited;
    private boolean guanyat;
    private Utils utils;

    public GameProtocol(Socket socket) throws IOException{
        this.sucked = socket;
        this.utils = new Utils(this.sucked);
        this.admited = false;
        this.guanyat = false;
    }

    public int receiveHelloAndSendReady() throws IOException{
        this.utils.read_Byte();
        this.id = this.utils.read_Int();
        String actionName = utils.convertToString();
        System.out.println("HELLO   C -------1 " + id + " " + actionName + "--> S");
        this.utils.writeReady(id);
        System.out.println("READY   C <------2 " + id + "--------- S");
        return 2;
    }

    public int receivePlayAndSendAdmit() throws IOException{
        while(!this.admited){
            this.guanyat = false;
            this.utils.read_Byte();
            int id_aux = this.utils.read_Int();
            System.out.println("PLAY    C -------3 " + id + "--------> S");
            if(id_aux != this.id){
                this.utils.errorMethod((byte)4);
                this.admited = false;
            }else{
                this.admited = true;
                this.utils.writeAdmit(this.admited);
            }
            System.out.println("ADMIT   C <------4 " + ((byte) (this.admited?1:0)) + "------------- S");
        }

        return 3;
    }

    public int reciveActionAndSendResult() throws IOException{
        while(!this.guanyat){
            this.utils.read_Byte();
            StringBuilder actionBuilder = new StringBuilder();
            for(int i = 0; i < 5; i++){
                char chars = this.utils.read_Char();
                actionBuilder.append(chars);
            }
            String actionName = actionBuilder.toString();
            System.out.println("ACTION  C -------5 " + actionName + "--------> S");
        
            String actionResult = this.utils.selectAction(actionName);
            if(actionResult.equals("ERROR")){
                this.utils.errorMethod((byte)3);
            }else{
                this.utils.writeResult(actionResult);
                System.out.println("RESULT  C <------6 " + actionResult + "--------- S");
                if(actionResult.equals("ENDS0") || actionResult.equals("ENDS1")){
                    this.guanyat = true;
                    this.admited = false;
                    utils.reiniciarBullets();
                    return 4;
                }
            }
        }
        return 4; 
    }


    



}