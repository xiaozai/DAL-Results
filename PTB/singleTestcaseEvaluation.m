function [succRate,TypeI,TypeII]=singleTestcaseEvaluation (resultpath,gt_path,seq_name,thresh)
%result fromat each line x1,x2,y1,y2,(state) for each frame
%resultpath path to result folder  './bear_front/'
%gt_path path to ground truch folder './bear_front/'
%thresh 1*N array overlap threshhold for a success e.g. [0:0.01:1]; or thresh=0.5 
%output success rate 1*N
%TypeI,TypeII error

result=dlmread([resultpath '/' seq_name '.txt']);
gt=dlmread([gt_path '/' seq_name '/' seq_name '.txt']);
gt(:,3:4)=gt(:,3:4)+gt(:,1:2);
result(:,3:4)=result(:,3:4)+result(:,1:2);
if size(gt,1)==size(result,1)
    numOfFrame=size(gt,1);
else
    numOfFrame=min(size(gt,1),size(result,1));
    gt=gt(1:numOfFrame,:);
    result=result(1:numOfFrame,:);
end

if size(result,2)==5,
    resultState=result(:,5); 
    result=result(:,1:4);
elseif size(result,2)==4,
    resultState=zeros(size(result,1));
else
    fprintf(['worng input fromat for: ' seq_name])
end
[ overlapErrArray,missOcc,missTar] = overlapErrorOcc( gt,result,resultState);
%succRate with different threshold
succRate=singleSR(overlapErrArray, thresh);
%type 1? 2 error
TypeI=missTar/numOfFrame;
TypeII=missOcc/numOfFrame;
end
function [ overlap,missOcc,missTar ] = overlapErrorOcc( A,B,state)
A=A';
B=B';
missOcc=0;
missTar=0;
for frameid= 1:size(A,2),
    if ~isnan(A(1,frameid))&&~isnan(B(1,frameid))
        overlap(frameid)= overlapSingle(A(:,frameid),B(:,frameid));
    elseif isnan(A(1,frameid))&& (state(frameid)==1||isnan(B(1,frameid)))
            overlap(frameid)=1;
    else
        overlap(frameid)=0;
        if ~isnan(A(1,frameid))&&isnan(B(1,frameid))
            missTar=missTar+1;
        end
        if isnan(A(1,frameid))&&~isnan(B(1,frameid))
            missOcc=missOcc+1;
        end
            
    end
end

end
function out= overlapSingle(bb1,bb2)
    if bb1(1) > bb2(3),out =0 ;return ;end
    if (bb1(2) > bb2(4)),out =0 ; return ; end
    if (bb1(3) < bb2(1)),out =0 ;return ; end
    if (bb1(4) < bb2(2)),out =0 ;return ; end

    b=min(bb1(3:4),bb2(3:4))-max(bb1(1:2),bb2(1:2));
    b(b<0)=0;
    intersection =b(1).*b(2);
    area1=(bb1(3)-bb1(1))*(bb1(4)-bb1(2));
    area2=(bb2(3)-bb2(1))*(bb2(4)-bb2(2));
    out = intersection/(area1 + area2 - intersection);
end
function sr = singleSR(overlap, thresh)
    sr = mean(repmat(overlap(:), [1 length(thresh)]) >= repmat(thresh(:)', [length(overlap) 1]));
end
