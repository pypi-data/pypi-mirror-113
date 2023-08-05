Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var utils_1 = require("app/components/events/interfaces/utils");
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var utils_2 = require("app/utils");
var getUnknownData_1 = tslib_1.__importDefault(require("../getUnknownData"));
var getUserKnownData_1 = tslib_1.__importDefault(require("./getUserKnownData"));
var types_1 = require("./types");
var userKnownDataValues = [
    types_1.UserKnownDataType.ID,
    types_1.UserKnownDataType.EMAIL,
    types_1.UserKnownDataType.USERNAME,
    types_1.UserKnownDataType.IP_ADDRESS,
    types_1.UserKnownDataType.NAME,
];
var userIgnoredDataValues = [types_1.UserIgnoredDataType.DATA];
function User(_a) {
    var data = _a.data;
    return (<div className="user-widget">
      <div className="pull-left">
        <userAvatar_1.default user={utils_1.removeFilterMaskedEntries(data)} size={48} gravatar={false}/>
      </div>
      <contextBlock_1.default data={getUserKnownData_1.default(data, userKnownDataValues)}/>
      <contextBlock_1.default data={getUnknownData_1.default(data, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(userKnownDataValues)), tslib_1.__read(userIgnoredDataValues)))}/>
      {utils_2.defined(data === null || data === void 0 ? void 0 : data.data) && (<errorBoundary_1.default mini>
          <keyValueList_1.default data={Object.entries(data.data).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
                return ({
                    key: key,
                    value: value,
                    subject: key,
                    meta: metaProxy_1.getMeta(data.data, key),
                });
            })} isContextData/>
        </errorBoundary_1.default>)}
    </div>);
}
exports.default = User;
//# sourceMappingURL=user.jsx.map