from numpy import array,arctan2,cos,sin,pi,sqrt,matmul,exp

class Univector:
    #% These functions are needed to develop the univector field, and can be found at the paper:
    #% "Evolutionary Univector Field-based Navigation with Collision Avoidance for Mobile Robot"

    def __init__(self):
        #? Constants learned from EP
        self.d_e=5.37
        self.k_r=4.15
        self.delta=4.57
        self.k_o=0.12
        self.d_min=4.3 #* => modified: EP = 3.48

    def rotMatrix(self,alpha):
        return array(((cos(alpha),-sin(alpha)),(sin(alpha),cos(alpha))))

    def phi_h_CW(self,x,y,xg,yg):
        rho=sqrt((x-xg)**2+(y-yg)**2)
        theta=arctan2(y-yg,x-xg)
        if rho > self.d_e:
            phi=theta+0.5*pi*(2-((self.d_e+self.k_r)/(rho+self.k_r)))
        else:
            phi=theta+0.5*pi*sqrt(rho/self.d_e)
        phi=arctan2(sin(phi),cos(phi)) #? Trick to mantain phi between [-pi,pi]
        return phi

    def phi_h_CCW(self,x,y,xg,yg):
        rho=sqrt((x-xg)**2+(y-yg)**2)
        theta=arctan2(y-yg,x-xg)
        if rho > self.d_e:
            phi=theta-0.5*pi*(2-((self.d_e+self.k_r)/(rho+self.k_r)))
        else:
            phi=theta-0.5*pi*sqrt(rho/self.d_e)
        phi=arctan2(sin(phi),cos(phi)) #? Trick to mantain phi between [-pi,pi]
        return phi

    def N_h(self,phi):
        return array([[cos(phi)],[sin(phi)]])

    def gaussianFunc(self,r):
        return exp(-0.5*(r/self.delta)**2)

    #% This is the hyperbolic vector field which yields us to the target position with the desired posture
    #% without avoiding any obstacle
    def hipVecField(self,robot,target):
        yl=robot.yPos+self.d_e
        yr=robot.yPos-self.d_e
        nCW=self.N_h(self.phi_h_CW(robot.xPos,robot.yPos+self.d_e,target.xPos,target.yPos))
        nCCW=self.N_h(self.phi_h_CCW(robot.xPos,robot.yPos-self.d_e,target.xPos,target.yPos))
        if (robot.yPos >= -self.d_e and robot.yPos < self.d_e):
            phi=0.5*(yl*nCCW+yr*nCW)/self.d_e
            phi=arctan2(phi[1],phi[0])
        elif (robot.yPos < -self.d_e):
            phi=self.phi_h_CW(robot.xPos,robot.yPos-self.d_e,target.xPos,target.yPos)
        else:
            phi=self.phi_h_CCW(robot.xPos,robot.yPos+self.d_e,target.xPos,target.yPos)
        return phi

    #% This is the 'N_Posture' vector field which yields us to the target position with the desired posture
    #% without avoiding any obstacle
    def nVecField(self,robot,target,n=8,d=2,haveFace=False):
        rx=target.xPos+d*cos(target.theta)
        ry=target.yPos+d*sin(target.theta)
        pgAng=arctan2(target.yPos-robot.yPos,target.xPos-robot.xPos)
        prAng=arctan2(ry-robot.yPos,rx-robot.xPos)
        alpha=arctan2(sin(prAng-pgAng),cos(prAng-pgAng))
        phi=arctan2(sin(pgAng-n*alpha),cos(pgAng-n*alpha))
        return phi

    #% This is the vector field which let us avoid a moving obstacle, but don't yields us to the target position
    def aoVecField(self,robot,obst):
        sx=self.k_o*(obst.v*cos(obst.theta)-robot.v*cos(robot.theta))   #? Components of the shifting vector, where
        sy=self.k_o*(obst.v*sin(obst.theta)-robot.v*sin(robot.theta))   #? S=k_o*(V_obst-V_robot)
        s=sqrt(sx**2+sy**2)
        d=robot.dist(obst)
        if d >= s:
            px=obst.xPos+sx
            py=obst.yPos+sy
        else:
            px=obst.xPos+(d/s)*sx
            py=obst.yPos+(d/s)*sy
        phi=arctan2(robot.yPos-py,robot.xPos-px)
        return phi

    #% This is the composed vector field, which mix both move-to-target (hyperbolic) and avoid-obstacle vector field
    #% using a gaussian function
    def univecField_H(self,robot,target,obst):
        d=robot.dist(obst)
        if (d <= self.d_min):
            phi=self.aoVecField(robot,obst)
            print('puro')
        else:
            phi=self.gaussianFunc(d-self.d_min)*self.aoVecField(robot,obst)
            phi+=(1-self.gaussianFunc(d-self.d_min))*self.hipVecField(robot,target)
        return phi

    #% This is the composed vector field, which mix both move-to-target ('N_Posture') and avoid-obstacle vector field
    #% using a gaussian function
    def univecField_N(self,robot,target,obst,n=8,d=2):
        if (robot.dist(obst) <= self.d_min):
            phi=self.aoVecField(robot,obst)
        else:
            phi=self.gaussianFunc(robot.dist(obst)-self.d_min)*self.aoVecField(robot,obst)
            phi+=(1-self.gaussianFunc(robot.dist(obst)-self.d_min))*self.nVecField(robot,target,n,d,haveFace=False)
        return phi
