difference(){
    import("RpiB+_screen32_screenframe.stl");
    translate([0,0,0]){
        cube([100,20,10]);
        cube([10,20,80]);
    }
    translate([100,0,0]){
        cube([11,20,80]);
    }
    translate([0,0,70]){
        cube([100,20,11]);
    }
}
translate([10,-17,10]){
    cube([90,17,1]);
}
translate([10,-17,69]){
    cube([90,17,1]);
}