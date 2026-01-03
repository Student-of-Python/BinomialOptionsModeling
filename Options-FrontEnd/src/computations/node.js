
export class Node {
    constructor (underlying_value){
    this.underlying_value = underlying_value;
    this.option_value = null;
    //Greeks
    this.delta = null;
    this.gamma = null; 
    this.theta = null;
    this.vega = null; 
    this.rho = null;
    }

    toString(){
    return [
        this.underlying_value != null && `S: ${this.underlying_value.toFixed(2)}`,
        this.option_value != null && `V: ${this.option_value.toFixed(2)}`,
        this.delta != null && `Δ: ${this.delta.toFixed(2)}`,
        this.gamma != null && `Γ: ${this.gamma.toFixed(2)}`,
        this.theta != null && `Θ: ${this.theta.toFixed(2)}`,
        this.vega != null && `Vega: ${this.vega.toFixed(2)}`,
        this.rho != null && `Rho: ${this.rho.toFixed(2)}`
    ].filter(Boolean).join("\n ");
 }
}