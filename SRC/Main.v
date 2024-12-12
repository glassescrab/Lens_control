`timescale 1ns / 1ps

module Main(   
    output [7:0] led,
    input sys_clkn,
    input sys_clkp,
    input  [3:0] button,
    output LENS_SPI_CLK,
    output LENS_SPI_MOSI,
    input LENS_SPI_MISO
);

    
    // Clock generation//////////////////////////////////////////////////////////////////
    reg ILA_Clk = 0;
    reg SPI_Module_Clk = 0;
    wire clk;
    reg [23:0] ClkDivILA = 24'd0;
    reg [23:0] ClkDivSPI = 24'd0;
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
    
    assign PC_val1 = 8'h12;
    assign PC_val2 = button[2] ? 8'h80 : 8'h7F;
    assign PC_wait1 = 8'h18;
    assign PC_wait2 = 8'h10;
    //SPI SERDES
    SPI_driver SPI_driver(
    .clk(SPI_Module_Clk),
    .cur_state(SPI_state),
    
    .SPI_MISO(LENS_SPI_MISO),
    .SPI_MOSI(LENS_SPI_MOSI),
    .SPI_CLK(LENS_SPI_CLK),
    .SPI_EN(LEN_EN),
    
    .busy(busy),
    .command_read(command_read),
    .rx_read(rx_read),
    .tx_read(tx_read),    
    .Spi_rw(Spi_rw),
    .Spi_rx_reg(Spi_rx_reg),
    .Spi_tx_reg(Spi_tx_reg),
    .Spi_wait_reg(Spi_wait_reg)
    );
    //SPI controller
    SPI_controller SPI_controller(
    .clk(SPI_Module_Clk),
    .PC_rx(~button),
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
        .probe1(~button),
        .probe2(LENS_SPI_CLK),
        .probe3(LENS_SPI_MOSI),
        .probe4(SPI_MISO)
        );
endmodule