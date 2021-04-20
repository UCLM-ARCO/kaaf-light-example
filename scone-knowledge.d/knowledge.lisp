(in-context {general})

(new-type {user} {person})
(new-type {room} {place})
(new-type {building element} {thing})
(new-type {light source} {thing})

(new-type {window} {building element})
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
(new-intersection-type {bulb} '({light source} {actuator}))

;; ########## RESOURCES ##########
(new-type {resource} {thing})
(new-is-a {information} {resource}) ;; already in the KB core
(new-is-a {event} {information})

(new-is-a {light} {resource})
(new-type {occupied room} {information})
(new-type {occupancy} {event})

;; ########## PROVISIONS/REQUIREMENTS ##########
(new-type-role {provider} {thing} {thing})
(new-type-role {location} {thing} {place})

(new-relation {indicate} ;; A indicates B. Ex: motion event indicates occupied room
        :a-inst-of {information}
        :b-inst-of {information}
        :c-inst-of {location})
    
(new-relation {require}  ;; A requires B. Ex: occupied room requires light
        :a-inst-of {information}
        :b-inst-of {resource}
        :c-inst-of {location})

;; ---------- Occupation
(new-indv {motion sensor:location} {place})
(x-is-the-y-of-z {motion sensor} {provider} {occupancy})
(x-is-the-y-of-z {motion sensor:location} {location} {motion sensor})
(new-statement {occupancy} {indicate} {occupied room} :c (the-x-of-y {location} (the-x-role-of-y {provider} {motion event})))

(new-indv {occupied room:location} {place})
(x-is-the-y-of-z {occupied room:location} {location} {occupied room})
(new-statement {occupied room} {require} {light} :c {occupied room:location})

;; ---------- Illumination
(x-is-the-y-of-z {bulb} {provider} {light})

(new-context {day} {general})
(new-context {night} {general})

(in-context {day})
(x-is-the-y-of-z {window} {provider} {light})
(in-context {night})
(x-is-not-the-y-of-z {window} {provider} {light})
(in-context {general})


