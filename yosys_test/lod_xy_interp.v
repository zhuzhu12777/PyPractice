//val_out = current*(right_value - left_value)*(adjust_value>>10) + left_value
module LOD_XY_INTERP(
    output  reg [9:0]   VAL_OUT,        //u0.10

    input               CLK,
    input               RSTB,

    input       [9:0]   CURRENT,        //u10.0
    input       [11:0]  GAIN,           //u0.12 adjust_gain = 1 / node2
    input       [7:0]   LEFT_VALUE,     //u0.8
    input       [7:0]   RIGHT_VALUE     //u0.8
);
// reg

// wire
wire signed [10:0]  CURRENT_S = $signed({1'b0, CURRENT});   //s11.0
wire signed [8:0]   VAL1      = $signed({1'b0, RIGHT_VALUE}) - $signed({1'b0, LEFT_VALUE});  //s1.8
reg  signed [18:0]  VAL2;   //s11.8
wire signed [31:0]  VAL3;   //s12.20
wire signed [21:0]  VAL4;   //s12.10
wire signed [21:0]  VAL5;   //s12.10

//assign VAL2 = VAL1 * CURRENT_S;
always@(posedge CLK or negedge RSTB) begin
    if(!RSTB)
        VAL2 <= #1 19'sd0;
    else
        VAL2 <= #1 VAL1 * CURRENT_S;
end

reg     [11:0] GAIN_1D;
reg     [7:0]  LEFT_VALUE_1D;
always@(posedge CLK or negedge RSTB) begin
    if(!RSTB) begin
        GAIN_1D <= #1 12'd0;
        LEFT_VALUE_1D <= #1 8'd0;
    end else begin
        GAIN_1D <= #1 GAIN;
        LEFT_VALUE_1D <= #1 LEFT_VALUE;
    end
end

wire        [12:0]  GAIN_ADD  = GAIN_1D + 1'b1;
wire signed [13:0]  GAIN_S = $signed({1'b0, GAIN_ADD});     //s2.12
assign VAL3 = VAL2 * GAIN_S;

assign VAL4 = $signed(VAL3[31:10]);  //s12.20 -> s12.10
assign VAL5 = VAL4 + $signed({1'b0, LEFT_VALUE_1D, 2'd0});

always@(posedge CLK or negedge RSTB) begin
    if(!RSTB)
        VAL_OUT <= #1 10'd0;
    else
        VAL_OUT <= #1 VAL5[21] ? 10'd0 : VAL5[10] ? 10'd1023 : VAL5[9:0];     //u1.9, min(left, right) <= val5 <= max(left, right)
end

// assertion here
`ifdef LOD_SVA
`include "std_ovl_defines.h"

wire chk_val5 = VAL5[21] ? ~&VAL5[20:11] : |VAL5[20:11];
assert_never #(0, 1, "XY_INTERP VAL5 is not right") U_CHK_VAL5(CLK, RSTB, chk_val5);

`endif

`ifdef LOD_SBY

wire chk_val5 = VAL5[21] ? ~&VAL5[20:11] : |VAL5[20:11];
reg rst_chk_en = 0;
always@(*) begin
    assume((CURRENT+1) * (GAIN+1) < 4096);
    assume(LEFT_VALUE < RIGHT_VALUE);
    assert(chk_val5 == 1'b0);
end

`endif


endmodule
