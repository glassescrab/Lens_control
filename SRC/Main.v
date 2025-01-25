`timescale 1ns / 1ps

module Main(   
    output [7:0] led,
    input sys_clkn,
    input sys_clkp,
    input  [3:0] button,
    output LENS_SPI_CLK,
    output LENS_SPI_MOSI,
    input LENS_SPI_MISO,
    input  [4:0] okUH,
    output [2:0] okHU,
    inout  [31:0] okUHU,
    inout  okAA      
);

    
    // Clock generation//////////////////////////////////////////////////////////////////
    reg ILA_Clk = 0;
    reg SPI_Module_Clk = 0;
    wire clk;
    reg [23:0] ClkDivILA = 24'd0;
    reg [23:0] ClkDivSPI = 24'd0;

    wire [31:0] SPI_control;
    wire [31:0] SPI_val;

    IBUFGDS osc_clk(
        .O(clk),
        .I(sys_clkp),
        .IB(sys_clkn)
    ); 
    always @(posedge clk) begin        
        if (ClkDivILA == 24) begin
            ILA_Clk <= !ILA_Clk;                       
            ClkDivILA <= 0;
        end else begin                        
            ClkDivILA <= ClkDivILA + 1'b1;
        end
    end
    always @(posedge clk) begin        
        if (ClkDivSPI == 24) begin
            SPI_Module_Clk <= !SPI_Module_Clk;                       
            ClkDivSPI <= 0;
        end else begin                        
            ClkDivSPI <= ClkDivSPI + 1'b1;
        end
    end
    wire [3:0] SPI_state;
    wire busy;
    wire command_read;
    wire rx_read;
    
//    wire  [3:0] button;
//    wire LENS_SPI_CLK;
//    wire LENS_SPI_MOSI;
//    wire LENS_SPI_MISO;
    wire tx_read;
    wire [1:0] Spi_rw;
    wire [7:0] Spi_rx_reg;
    wire [7:0] Spi_tx_reg;
    wire [15:0] Spi_wait_reg;
    wire [31:0]     PC_val1;
    wire [31:0]     PC_val2;
    wire [31:0]     PC_tx;
    wire [31:0]     PC_wait1;
    wire [31:0]     PC_wait2;
    wire LEN_EN;
//    wire [31:0] SPI_temp;
    assign PC_val1 = SPI_control[31:24];
    assign PC_val2 = SPI_control[15:8];
    assign PC_wait1 = SPI_control[23:17];
    assign PC_wait2 = SPI_control[7:1];
    //SPI SERDES
    SPI_driver SPI_driver(
    .clk(SPI_Module_Clk),
    .cur_state(SPI_state),
    
    .SPI_MISO(LENS_SPI_MISO),
    .SPI_MOSI(LENS_SPI_MOSI),
    .SPI_CLK(LENS_SPI_CLK),
    .SPI_EN(LEN_EN),
//    .PC_tx(SPI_val),
    .busy(busy),
    .command_read(command_read),
    .rx_read(rx_read),
    .tx_read(tx_read),    
    .Spi_rw(Spi_rw),
    .Spi_rx_reg(Spi_rx_reg),
    .Spi_tx_reg(Spi_tx_reg),
    .Spi_wait_reg(Spi_wait_reg)
    );

    wire okClk;            //These are FrontPanel wires needed to IO communication    
    wire [112:0]    okHE;  //These are FrontPanel wires needed to IO communication    
    wire [64:0]     okEH;  //These are FrontPanel wires needed to IO communication
   
    //This is the OK host that allows data to be sent or recived    
    okHost hostIF (
        .okUH(okUH),
        .okHU(okHU),
        .okUHU(okUHU),
        .okClk(okClk),
        .okAA(okAA),
        .okHE(okHE),
        .okEH(okEH)
    );
//    okTriggerIn  trig40 (  .okHE(okHE),
//        .ep_addr(8'h48),
//        .ep_clk(SPI_Module_Clk),
//        .ep_trigger(SPI_control));
    okWireIn wire10 (   .okHE(okHE), 
                        .ep_addr(8'h00), 
                        .ep_dataout(SPI_control));
    localparam endPt_count = 1;
    wire [endPt_count*65-1:0] okEHx;
    okWireOR # (.N(endPt_count)) wireOR (okEH, okEHx);


//    okTriggerOut trig60 ( .okHE(okHE),
//        .okEH(okEH),
//        .ep_addr(8'h60),
//        .ep_clk(SPI_Module_Clk),
//        .ep_trigger(SPI_temp));

    //SPI controller
    SPI_controller SPI_controller(
    .clk(SPI_Module_Clk),
    .PC_rx({2'b0,SPI_control[16],SPI_control[0]}),
    .PC_val1(PC_val1),
    .PC_val2(PC_val2),
    .PC_tx(PC_tx),
    .PC_wait1(PC_wait1),
    .PC_wait2(PC_wait2),
    .command_read(command_read),
    .rx_read(rx_read),
    .tx_read(tx_read),
    .rw(Spi_rw),
    .tx_byte(Spi_tx_reg),
    .rx_byte(Spi_rx_reg),
    .wait_byte(Spi_wait_reg),
    .busy(busy)
    );
    wire SPI_MISO;
    assign SPI_MISO = LENS_SPI_MISO;
    //Instantiate the ILA module
    ila_0 ila_sample12 ( 
        .clk(clk),
        .probe0(SPI_state),
        .probe1(SPI_control),
        .probe2(LENS_SPI_CLK),
        .probe3(LENS_SPI_MOSI),
        .probe4(SPI_MISO)
        );

endmodule