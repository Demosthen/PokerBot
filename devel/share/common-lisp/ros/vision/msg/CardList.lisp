; Auto-generated. Do not edit!


(cl:in-package vision-msg)


;//! \htmlinclude CardList.msg.html

(cl:defclass <CardList> (roslisp-msg-protocol:ros-message)
  ((cards
    :reader cards
    :initarg :cards
    :type (cl:vector cl:string)
   :initform (cl:make-array 0 :element-type 'cl:string :initial-element ""))
   (coords
    :reader coords
    :initarg :coords
    :type (cl:vector geometry_msgs-msg:Point)
   :initform (cl:make-array 0 :element-type 'geometry_msgs-msg:Point :initial-element (cl:make-instance 'geometry_msgs-msg:Point)))
   (count
    :reader count
    :initarg :count
    :type cl:fixnum
    :initform 0))
)

(cl:defclass CardList (<CardList>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CardList>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CardList)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name vision-msg:<CardList> is deprecated: use vision-msg:CardList instead.")))

(cl:ensure-generic-function 'cards-val :lambda-list '(m))
(cl:defmethod cards-val ((m <CardList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision-msg:cards-val is deprecated.  Use vision-msg:cards instead.")
  (cards m))

(cl:ensure-generic-function 'coords-val :lambda-list '(m))
(cl:defmethod coords-val ((m <CardList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision-msg:coords-val is deprecated.  Use vision-msg:coords instead.")
  (coords m))

(cl:ensure-generic-function 'count-val :lambda-list '(m))
(cl:defmethod count-val ((m <CardList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision-msg:count-val is deprecated.  Use vision-msg:count instead.")
  (count m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CardList>) ostream)
  "Serializes a message object of type '<CardList>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'cards))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((__ros_str_len (cl:length ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) ele))
   (cl:slot-value msg 'cards))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'coords))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'coords))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'count)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CardList>) istream)
  "Deserializes a message object of type '<CardList>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'cards) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'cards)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:aref vals i) __ros_str_idx) (cl:code-char (cl:read-byte istream))))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'coords) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'coords)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'geometry_msgs-msg:Point))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'count)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CardList>)))
  "Returns string type for a message object of type '<CardList>"
  "vision/CardList")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CardList)))
  "Returns string type for a message object of type 'CardList"
  "vision/CardList")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CardList>)))
  "Returns md5sum for a message object of type '<CardList>"
  "995f141894c990e15bdbb5ec7c1d8be3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CardList)))
  "Returns md5sum for a message object of type 'CardList"
  "995f141894c990e15bdbb5ec7c1d8be3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CardList>)))
  "Returns full string definition for message of type '<CardList>"
  (cl:format cl:nil "string[] cards~%geometry_msgs/Point[] coords~%uint8 count~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CardList)))
  "Returns full string definition for message of type 'CardList"
  (cl:format cl:nil "string[] cards~%geometry_msgs/Point[] coords~%uint8 count~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CardList>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'cards) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4 (cl:length ele))))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'coords) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CardList>))
  "Converts a ROS message object to a list"
  (cl:list 'CardList
    (cl:cons ':cards (cards msg))
    (cl:cons ':coords (coords msg))
    (cl:cons ':count (count msg))
))
