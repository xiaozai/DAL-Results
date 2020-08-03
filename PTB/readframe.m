clear all
directory = './EvaluationSet/bag1/';
load([directory 'frames']);

%K is [fx 0 cx; 0 fy cy; 0 0 1];
K = frames.K;
cx = K(1,3);cy = K(2,3);
fx = K(1,1);fy = K(2,2);

numOfFrames = frames.length;
imageNames = cell(1,numOfFrames*2);
XYZcam = zeros(480,640,4,numOfFrames);

for frameId = 1:numOfFrames
    imageName = fullfile(directory,sprintf('rgb/r-%d-%d.png', frames.imageTimestamp(frameId), frames.imageFrameID(frameId)));
    rgb = imread(imageName);
    depthName = fullfile(directory,sprintf('depth/d-%d-%d.png', frames.depthTimestamp(frameId), frames.depthFrameID(frameId)));
    depth = imread(depthName);
    depth = bitor(bitshift(depth,-3), bitshift(depth,16-3));
    depth = double(depth);
    %show the 2D image
    subplot(1,2,1); imshow(rgb);
    subplot(1,2,2); imshow(depth);
    
    %3D point for the frame
    depthInpaint = depth/1000;
    [x,y] = meshgrid(1:640, 1:480); 
    Xworld = (x-cx).*depthInpaint*1/fx;
    Yworld = (y-cy).*depthInpaint*1/fy;
    Zworld = depthInpaint;
    validM = depth~=0;
    XYZworldframe = [Xworld(:)'; Yworld(:)'; Zworld(:)'];
    valid = validM(:)';   
    
    % XYZworldframe 3xn and RGB 3xn
    RGB = [reshape(rgb(:,:,1),1,[]);reshape(rgb(:,:,2),1,[]);reshape(rgb(:,:,3),1,[])];
    XYZpoints = XYZworldframe(:,valid);
    RGBpoints = RGB(:,valid);
    
    % display in 3D: subsample to avoid too much to display.
    sample_gap=20;
    XYZpoints = XYZpoints(:,1:sample_gap:end);
    RGBpoints = RGBpoints(:,1:sample_gap:end);
    figure, scatter3(XYZpoints(1,:),XYZpoints(2,:),XYZpoints(3,:),ones(1,size(XYZpoints,2)),double(RGBpoints)'/255,'filled');
    axis equal; view(0,-90);
    pause;
end