// Auto-generated. Do not edit!

// (in-package vision.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class CardList {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.cards = null;
      this.coords = null;
      this.count = null;
    }
    else {
      if (initObj.hasOwnProperty('cards')) {
        this.cards = initObj.cards
      }
      else {
        this.cards = [];
      }
      if (initObj.hasOwnProperty('coords')) {
        this.coords = initObj.coords
      }
      else {
        this.coords = [];
      }
      if (initObj.hasOwnProperty('count')) {
        this.count = initObj.count
      }
      else {
        this.count = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type CardList
    // Serialize message field [cards]
    bufferOffset = _arraySerializer.string(obj.cards, buffer, bufferOffset, null);
    // Serialize message field [coords]
    // Serialize the length for message field [coords]
    bufferOffset = _serializer.uint32(obj.coords.length, buffer, bufferOffset);
    obj.coords.forEach((val) => {
      bufferOffset = geometry_msgs.msg.Point.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [count]
    bufferOffset = _serializer.uint8(obj.count, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type CardList
    let len;
    let data = new CardList(null);
    // Deserialize message field [cards]
    data.cards = _arrayDeserializer.string(buffer, bufferOffset, null)
    // Deserialize message field [coords]
    // Deserialize array length for message field [coords]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.coords = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.coords[i] = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [count]
    data.count = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.cards.forEach((val) => {
      length += 4 + val.length;
    });
    length += 24 * object.coords.length;
    return length + 9;
  }

  static datatype() {
    // Returns string type for a message object
    return 'vision/CardList';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '995f141894c990e15bdbb5ec7c1d8be3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string[] cards
    geometry_msgs/Point[] coords
    uint8 count
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new CardList(null);
    if (msg.cards !== undefined) {
      resolved.cards = msg.cards;
    }
    else {
      resolved.cards = []
    }

    if (msg.coords !== undefined) {
      resolved.coords = new Array(msg.coords.length);
      for (let i = 0; i < resolved.coords.length; ++i) {
        resolved.coords[i] = geometry_msgs.msg.Point.Resolve(msg.coords[i]);
      }
    }
    else {
      resolved.coords = []
    }

    if (msg.count !== undefined) {
      resolved.count = msg.count;
    }
    else {
      resolved.count = 0
    }

    return resolved;
    }
};

module.exports = CardList;
