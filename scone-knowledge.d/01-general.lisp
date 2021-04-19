(in-context {general})

(new-type {user} {person})
(new-type {room} {place})

(new-type {light source} {thing})

(new-type {window} {thing})
(new-is-a {window} {light source})

;; ########## DEVICES ##########
(new-type {device} {thing})
(new-intersection-type {service} '({device} {intangible}))
(new-intersection-type {transducer} '({device} {physical object}))
(new-type {sensor} {transducer})
(new-type {actuator} {transducer})

;; ---------- Sensors
(new-type {light sensor} {sensor})
(new-type {motion sensor} {sensor})
(new-type {door sensor} {sensor})

;; ---------- Actuators
(new-intersection-type {lamp} '({light source} {actuator}))

;; ########## RESOURCES ##########
(new-type {light} {thing})
