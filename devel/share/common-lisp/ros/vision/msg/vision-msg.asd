
(cl:in-package :asdf)

(defsystem "vision-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "CardList" :depends-on ("_package_CardList"))
    (:file "_package_CardList" :depends-on ("_package"))
  ))