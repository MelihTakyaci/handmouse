class ROIManager:
    def __init__(self, screen_width, screen_height, cam_width=640, cam_height=480, scale=0.8):
        self.cam_width = cam_width
        self.cam_height = cam_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.roi_h = int(cam_height * scale)
        self.roi_w = int(self.roi_h * (screen_width / screen_height))
        self.roi_x = int((cam_width - self.roi_w) // 2)
        self.roi_y = 1

    def update_roi(self, frame_width, frame_height, key, zoom_step=10, move_step=10):
        """
        Klavye girdilerine göre ROI boyut ve konum ayarlaması yapar.
        'i'/'o' ile zoom, 'w', 's', 'a', 'd' ile hareket ayarlanır.
        """
        if key == ord('i'):
            self.roi_w = max(100, self.roi_w - zoom_step)
            self.roi_h = max(100, self.roi_h - zoom_step)
        elif key == ord('o'):
            self.roi_w = min(frame_width - self.roi_x, self.roi_w + zoom_step)
            self.roi_h = min(frame_height - self.roi_y, self.roi_h + zoom_step)
        elif key == ord('w'):
            self.roi_y = max(0, self.roi_y - move_step)
        elif key == ord('s'):
            self.roi_y = min(frame_height - self.roi_h, self.roi_y + move_step)
        elif key == ord('a'):
            self.roi_x = max(0, self.roi_x - move_step)
        elif key == ord('d'):
            self.roi_x = min(frame_width - self.roi_w, self.roi_x + move_step)