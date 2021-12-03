;; Auto-generated. Do not edit!


(when (boundp 'vision::CardList)
  (if (not (find-package "VISION"))
    (make-package "VISION"))
  (shadow 'CardList (find-package "VISION")))
(unless (find-package "VISION::CARDLIST")
  (make-package "VISION::CARDLIST"))

(in-package "ROS")
;;//! \htmlinclude CardList.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass vision::CardList
  :super ros::object
  :slots (_cards _coords _count ))

(defmethod vision::CardList
  (:init
   (&key
    ((:cards __cards) (let (r) (dotimes (i 0) (push "" r)) r))
    ((:coords __coords) (let (r) (dotimes (i 0) (push (instance geometry_msgs::Point :init) r)) r))
    ((:count __count) 0)
    )
   (send-super :init)
   (setq _cards __cards)
   (setq _coords __coords)
   (setq _count (round __count))
   self)
  (:cards
   (&optional __cards)
   (if __cards (setq _cards __cards)) _cards)
  (:coords
   (&rest __coords)
   (if (keywordp (car __coords))
       (send* _coords __coords)
     (progn
       (if __coords (setq _coords (car __coords)))
       _coords)))
  (:count
   (&optional __count)
   (if __count (setq _count __count)) _count)
  (:serialization-length
   ()
   (+
    ;; string[] _cards
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _cards)) 4
    ;; geometry_msgs/Point[] _coords
    (apply #'+ (send-all _coords :serialization-length)) 4
    ;; uint8 _count
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string[] _cards
     (write-long (length _cards) s)
     (dolist (elem _cards)
       (write-long (length elem) s) (princ elem s)
       )
     ;; geometry_msgs/Point[] _coords
     (write-long (length _coords) s)
     (dolist (elem _coords)
       (send elem :serialize s)
       )
     ;; uint8 _count
       (write-byte _count s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string[] _cards
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _cards (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _cards i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;; geometry_msgs/Point[] _coords
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _coords (let (r) (dotimes (i n) (push (instance geometry_msgs::Point :init) r)) r))
     (dolist (elem- _coords)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; uint8 _count
     (setq _count (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get vision::CardList :md5sum-) "995f141894c990e15bdbb5ec7c1d8be3")
(setf (get vision::CardList :datatype-) "vision/CardList")
(setf (get vision::CardList :definition-)
      "string[] cards
geometry_msgs/Point[] coords
uint8 count

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

")



(provide :vision/CardList "995f141894c990e15bdbb5ec7c1d8be3")


