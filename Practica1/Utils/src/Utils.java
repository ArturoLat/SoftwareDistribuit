import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Random;

public class Utils {
    private DataOutputStream dataOutputStream;
    private DataInputStream dataInputStream;
    private int bullets_client;
    private int bullets_server;
    private String resposta;
    private int estat;

    public Utils(Socket socket) throws IOException {
        this.dataOutputStream = new DataOutputStream(socket.getOutputStream());
        this.dataInputStream = new DataInputStream(socket.getInputStream());
        this.bullets_server = 0;
        this.bullets_client = 0;
        this.resposta = "";
    }

    public DataOutputStream getDataOutputStream(){
        return this.dataOutputStream;
    }
    public DataInputStream getDataInputStream(){
        return this.dataInputStream;
    }

    public int getBullets_client(){
        return this.bullets_client;
    }

    public int getBullets_server(){
        return this.bullets_server;
    }

    public void errorMethod(Byte errCode) throws IOException{
        String message;
        if(errCode == 1){
            message = "CARÀCTER NO RECONEGUT";
        }else if(errCode == 2){
            message = "MISSATGE DESCONEGUT";
        }else if(errCode == 3){
            message = "MISSATGE FORA DE PROTOCOL";
        }else if(errCode == 4){
            message = "INICI DE SESSIO INCORRECTE";
        }else if(errCode == 5){
            message = "PARAULA DESCONEGUDA";
        }else if(errCode == 6){
            message = "MISSATGE MAL FORMAT";
        }else{
            message = "ERROR DESCONEGUT";
        }
        this.dataOutputStream.writeByte(8);
        this.dataOutputStream.writeByte(errCode);
        this.dataOutputStream.writeChars(message);
        this.dataOutputStream.writeByte(0);
        this.dataOutputStream.writeByte(0);
        this.dataOutputStream.flush();
        System.out.println("ERROR   C <------8 " + errCode + ", '" + message + "' -------- S");
    }

    public String selectAction(String actionName) throws IOException{
        String serverAction = serverAction();
        String result;
        if(actionName.equals("CHARG")){
            this.bullets_client++;
            if(serverAction.equals("CHARG")){
                result = "PLUS2"; //PLUS2
            }else if(serverAction.equals("SHOOT")){
                result = "ENDS0"; //ENDS0
            }else{
                result = "PLUS1"; //PLUS1
            }
        }else if(actionName.equals("SHOOT")){
            if(this.bullets_client == 0){
                if(serverAction.equals("CHARG")){ //Aixi si hi ha un error, no recarga
                    this.bullets_server--;
                }
                result = "ERROR";
            }else{
                this.bullets_client--;
                if(serverAction.equals("SHOOT")){
                    result = "DRAW0"; //DRAW0
                }else if(serverAction.equals("CHARG")){
                    result = "ENDS1"; //ENDS1
                }else{
                    result = "SAFE0"; //SAFE0
                }
            }
        }else{
            if(serverAction.equals("SHOOT")){
                result = "SAFE1"; //SAFE1
            }else if(serverAction.equals("CHARG")){
                result = "PLUS0"; //PLUS0
            }else{
                result = "SAFE2"; //SAFE2
            }
        }

        return result;
    }

    private String serverAction(){
        if(this.bullets_server==0){
            this.bullets_server++;
            return "CHARG";
        }else{
            Random rand  = new Random();
            int action = (int) rand.nextInt(2)+1;
            if(action==1){
                return "BLOCK";
            }else{
                this.bullets_server--;
                return "SHOOT";
            }
        }
    }

    public String convertToString() throws IOException {
        StringBuilder actionBuilder = new StringBuilder();
        char chars = read_Char();
        while(chars != 0){
            actionBuilder.append(chars);
            chars = read_Char();
        }
        String actionName = actionBuilder.toString();
        return actionName;
    }
    public void writeHello(int id, String name) throws IOException{
        this.dataOutputStream.writeByte(1);
        this.dataOutputStream.writeInt(id);
        this.dataOutputStream.writeChars(name);
        this.dataOutputStream.writeByte(0);
        this.dataOutputStream.writeByte(0);
        this.dataOutputStream.flush();
    }

    public void writeReady(int id) throws IOException {
        this.dataOutputStream.writeByte(2);
        this.dataOutputStream.writeInt(id);
        this.dataOutputStream.flush();
    }

    public void writePlay(int id) throws IOException{
        this.dataOutputStream.writeByte(3);
        this.dataOutputStream.writeInt(id);
        this.dataOutputStream.flush();
    }

    public void writeAdmit(Boolean admited) throws IOException{
        this.dataOutputStream.writeByte(4);
        this.dataOutputStream.writeBoolean(admited);
        this.dataOutputStream.flush();
    }

    public void writeAction(String actiontext) throws IOException{
        this.dataOutputStream.writeByte(5);
        this.dataOutputStream.writeChars(actiontext);
        this.dataOutputStream.flush();
    }

    public void writeResult(String actionResult) throws IOException{
        this.dataOutputStream.writeByte(6);
        this.dataOutputStream.writeChars(actionResult);
        this.dataOutputStream.flush();
    }

    public byte read_Byte() throws IOException{
        return this.dataInputStream.readByte();
    }

    public int read_Int() throws IOException{
        return this.dataInputStream.readInt();
    }

    public String read_String() throws IOException{
        return this.dataInputStream.readUTF();
    }

    public char read_Char() throws IOException{
        return this.dataInputStream.readChar();
    }

    public boolean read_Boolean() throws IOException{
        return this.dataInputStream.readBoolean();
    }

    public int write_Estat(String respostEstat){
        this.resposta = respostEstat;
        if(respostEstat.equals("S")){
            this.estat = 3;
        }else{
            this.estat = 5;
        }
        return estat;
    }

    public void reiniciarBullets(){
        this.bullets_client = 0;
        this.bullets_server = 0;
    }

    public String getResposta(){
        return this.resposta;
    }
    public static void main(String[] args) {

    }
}
