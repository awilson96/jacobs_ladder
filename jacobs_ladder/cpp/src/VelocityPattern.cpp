#include <cassert>
#include <iostream>

#include "VelocityPattern.h"

VelocityPattern::VelocityPattern(VelocityPatternData &vpd)
    : mName(vpd.name),
      mRepeatNum(vpd.repeatNum),
      mCrop(vpd.crop),
      mDynamics(vpd.dynamics),
      mDynamicsInt(vpd.dynamicsInt)
{
    assert(mDynamics.empty() || mDynamicsInt.empty());
    assert(mRepeatNum >= 0);
    if (mRepeatNum >= 1) {
        if (!mDynamics.empty()) {
            std::vector<VelocityDynamics> originalDynamics = mDynamics;
            mDynamics.reserve(mDynamics.size() + mRepeatNum * mDynamics.size());
            
            for (uint32_t i = 0; i < mRepeatNum; i++) {
                mDynamics.insert(mDynamics.end(), originalDynamics.begin(), originalDynamics.end());
            }
        }
        else if (!mDynamicsInt.empty()) {
            std::vector<int> originalDynamics = mDynamicsInt;
            mDynamicsInt.reserve(mDynamicsInt.size() + mRepeatNum * mDynamicsInt.size());
            
            for (uint32_t i = 0; i < mRepeatNum; i++) {
                mDynamicsInt.insert(mDynamicsInt.end(), originalDynamics.begin(), originalDynamics.end());
            }
        }
    }

    if (!mCrop.empty()) {
        size_t cropLength = mCrop.size();
        if (!mDynamics.empty()) {
            assert(cropLength <= mDynamics.size());
            mDynamics.resize(cropLength);
        }
        else if (!mDynamicsInt.empty()) {
            assert(cropLength <= mDynamicsInt.size());
            mDynamicsInt.resize(cropLength);
        }
        else {
            std::cout << "Error: No cropping was done since both dynamics vectors were empty" << std::endl;
        }
    }
}

VelocityPattern::~VelocityPattern() {}

std::string VelocityPattern::getName() {
    return mName;
}

uint32_t VelocityPattern::getNumberOfBeats() {
    if (!mDynamics.empty()) {
        return mDynamics.size();
    } 
    else if (!mDynamicsInt.empty()) {
        return mDynamicsInt.size();
    }
    else {
        return 0u;
    }
}

const VelocityPatternData VelocityPattern::getVelocityPatternData() {
    return VelocityPatternData(mName, mRepeatNum, mCrop, mDynamics, mDynamicsInt);
}

