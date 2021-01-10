import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

bariImg = mpimg.imread('groupGray.jpg')
chotiImg = mpimg.imread('boothiGray.jpg')

rows_bariImg = len(bariImg)
columns_bariImg = len(bariImg[0])

rows_chotiImg = len(chotiImg)
columns_chotiImg = len(chotiImg[0])

populationSize = 500
threshold = 0.8
generation = 0

def slice(x, y):
	return bariImg[x:x+rows_chotiImg, y:y+columns_chotiImg]

def bestfit(xlist, ylist):
	
	correlationList = []
	
	for i in range(populationSize):
		subImg = slice(xlist[i], ylist[i])
		correlationList.append(scipy.stats.kendalltau(chotiImg, subImg).correlation)
	
	for i in range(populationSize):
		positionBestfit = np.where(correlationList == np.amax(correlationList[i:]))
		
		temp = correlationList[i]
		correlationList[i] = correlationList[positionBestfit[0][0]]
		correlationList[positionBestfit[0][0]] = temp
		
		temp = xlist[i]
		xlist[i] = xlist[positionBestfit[0][0]]
		xlist[positionBestfit[0][0]] = temp
		
		temp = ylist[i]
		ylist[i] = ylist[positionBestfit[0][0]]
		ylist[positionBestfit[0][0]] = temp
	
	return xlist, ylist, correlationList

def binary(decimalNumber):
	return bin(decimalNumber)[2:]

def invert(binaryNumber):
	
	list1 = list(binaryNumber)
	
	index = np.random.randint(len(binaryNumber)-1)
	
	if list1[index] == '1':
		list1[index] = '0'
	else:
		list1[index] = '1'
	
	inverted_binaryNumber = ''.join(list1)
	
	return inverted_binaryNumber

def concatenate(P_x, P_y):
	
	list1 = list(P_x)
	list2 = list(P_y)
	
	X_maxbits = len(binary(1024))
	Y_maxbits = len(binary(512))

	# insert 0 in at zero index on every iteration
	for i in range(X_maxbits-len(list1)):
		list1.insert(0, '0')
	for i in range(Y_maxbits-len(list2)):
		list2.insert(0, '0')

	lenP_x = len(list1)
	lenP_y = len(list2)
	
	for i in range(len(list2)):
		list1.append(list2[i])
	
	concatenatedNumber = ''.join(list1)
	
	return concatenatedNumber, lenP_x, lenP_y

def replaceBit(P1_concatenatedNumber, P2_concatenatedNumber):
	list1 = list(P1_concatenatedNumber)
	list2 = list(P2_concatenatedNumber)

	randomIndex = np.random.randint(len(P1_concatenatedNumber)-1)

	for i in range(len(P1_concatenatedNumber)):
		if i < randomIndex:
			continue
		
		temp = list2[i]
		list2[i] = list1[i]
		list1[i] = temp

	P1_concatenatedNumber = ''.join(list1)
	P2_concatenatedNumber = ''.join(list2)
	
	return P1_concatenatedNumber, P2_concatenatedNumber

def crossRelation(P1_x, P1_y, P2_x, P2_y):
	
	P1_concatenatedNumber, lenP1_x, lenP1_y = concatenate(P1_x, P1_y)
	P2_concatenatedNumber, lenP2_x, lenP2_y = concatenate(P2_x, P2_y)
	
	P1, P2 = replaceBit(P1_concatenatedNumber, P2_concatenatedNumber)
	
	return P1, P2, lenP1_x, lenP2_x

def mutation(P1, P2, lenP1_x, lenP2_x):
	
	C1 = invert(P1)
	C2 = invert(P2)
	
	list1 = list(C1)
	list2 = list(C2)
	
	list1_x = []
	list1_y = []
	
	list2_x = []
	list2_y = []
	
	for i in range(len(list1)):
		if i >= lenP1_x:
			list1_y.append(list1[i])
		else:
			list1_x.append(list1[i])
	
	for i in range(len(list2)):
		if i >= lenP2_x:
			list2_y.append(list2[i])
		else:
			list2_x.append(list2[i])
	
	C1_x = ''.join(list1_x)
	C1_y = ''.join(list1_y)
	
	C2_x = ''.join(list2_x)
	C2_y = ''.join(list2_y)

	C1_x = int(C1_x, 2)
	
	if C1_x > (rows_bariImg - rows_chotiImg):
		C1_x = np.random.randint(rows_bariImg - rows_chotiImg)
	
	C1_y = int(C1_y, 2)
	
	if C1_y > (columns_bariImg - columns_chotiImg):
		C1_y = np.random.randint(columns_bariImg - columns_chotiImg)
	
	C2_x = int(C2_x, 2)
	
	if C2_x > (rows_bariImg - rows_chotiImg):
		C2_x = np.random.randint(rows_bariImg - rows_chotiImg)
	
	C2_y = int(C2_y, 2)
	
	if C2_y > (columns_bariImg - columns_chotiImg):
		C2_y = np.random.randint(columns_bariImg - columns_chotiImg)
	
	return C1_x, C1_y, C2_x, C2_y

def loop(xlist, ylist):
	
	x_list, y_list, correlationList = bestfit(xlist, ylist)

	global generation
	
	while True:

		print("Generation No.", generation)
		print("Correlation", correlationList[0])
		
		if round(correlationList[0], 1) == threshold:
			break
		
		if generation == 1500:
			return [], [], []
		
		generation += 1
		
		for i in range(0, populationSize, 2):
			P1_x = binary(x_list[i])
			P1_y = binary(y_list[i])
			
			P2_x = binary(x_list[i+1])
			P2_y = binary(y_list[i+1])
			
			P1, P2, lenP1_x, lenP2_x = crossRelation(P1_x, P1_y, P2_x, P2_y)
			
			C1_x, C1_y, C2_x, C2_y = mutation(P1, P2, lenP1_x, lenP2_x)
			
			x_list[i] = C1_x
			y_list[i] = C1_y
			
			x_list[i+1] = C2_x
			y_list[i+1] = C2_y
		
		x_list, y_list, correlationList = bestfit(x_list, y_list)
	
	return x_list, y_list, correlationList

def main():
	xlist = []
	ylist = []

	[xlist.append(np.random.randint(rows_bariImg - rows_chotiImg)) for i in range(populationSize)]
	[ylist.append(np.random.randint(columns_bariImg - columns_chotiImg)) for i in range(populationSize)]

	x_list, y_list, correlationList = loop(xlist, ylist)
	
	if x_list == [] and y_list == [] and correlationList == []:
		print("Not found.")
	else:
		print("x coordiante", y_list[0])
		print("y coordiante", x_list[0])
		fig, ax = plt.subplots(1)
		rect = patches.Rectangle((y_list[0], x_list[0]), columns_chotiImg, rows_chotiImg, linewidth=2, edgecolor='b', fill=False)

		ax.imshow(bariImg, cmap="gray")
		ax.add_patch(rect)

		plt.show()

main()