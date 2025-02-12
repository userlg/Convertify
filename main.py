from src.helpers import methods as m

if __name__ == '__main__':
    
    file = 'vid0001.avi'

    m.converting_video(file)

    print(m.verify_avi_format(file))