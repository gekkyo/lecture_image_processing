% �ۑ�W ���x�����O
% ��l�����ꂽ�摜�̘A�������Ƀ��x��������D
% ���L�̓T���v���v���O�����ł���D
% �ۑ�쐬�ɂ������ẮuLenna�v�ȊO�̉摜��p����D
% ��

ORG = imread('Lenna.png'); % �摜�ǂݍ���
ORG = rgb2gray(ORG); % ����2�W�摜�ɕϊ�
imagesc(ORG); colormap(gray); colorbar; % �摜�\��
pause;

IMG = ORG > 128; % 臒l128
imagesc(IMG); colormap(gray); colorbar; % �摜�\��
pause;

IMG = bwlabeln(IMG);
imagesc(IMG); colormap(jet); colorbar; % �摜�\��
pause;

