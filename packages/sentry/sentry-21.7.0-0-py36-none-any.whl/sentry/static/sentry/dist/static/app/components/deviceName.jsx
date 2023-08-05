Object.defineProperty(exports, "__esModule", { value: true });
exports.loadDeviceListModule = exports.deviceNameMapper = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
function deviceNameMapper(model, iOSDeviceList) {
    var modelIdentifier = model.split(' ')[0];
    var modelId = model.split(' ').splice(1).join(' ');
    var modelName = iOSDeviceList.generationByIdentifier(modelIdentifier);
    return modelName === undefined ? model : modelName + ' ' + modelId;
}
exports.deviceNameMapper = deviceNameMapper;
function loadDeviceListModule() {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        return tslib_1.__generator(this, function (_a) {
            return [2 /*return*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('ios-device-list')); })];
        });
    });
}
exports.loadDeviceListModule = loadDeviceListModule;
/**
 * This is used to map iOS Device Names to model name.
 * This asynchronously loads the ios-device-list library because of its size
 */
var DeviceName = /** @class */ (function (_super) {
    tslib_1.__extends(DeviceName, _super);
    function DeviceName(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            iOSDeviceList: null,
        };
        return _this;
    }
    DeviceName.prototype.componentDidMount = function () {
        var _this = this;
        // This is to handle react's warning on calling setState for unmounted components
        // Since we can't cancel promises, we need to do this
        this._isMounted = true;
        // This library is very big, so we are codesplitting it based on size and
        // the relatively small utility this library provides
        loadDeviceListModule().then(function (iOSDeviceList) {
            if (!_this._isMounted) {
                return;
            }
            _this.setState({ iOSDeviceList: iOSDeviceList });
        });
    };
    DeviceName.prototype.componentWillUnmount = function () {
        this._isMounted = false;
    };
    DeviceName.prototype.render = function () {
        var _a = this.props, value = _a.value, children = _a.children;
        var iOSDeviceList = this.state.iOSDeviceList;
        // value can be undefined, need to return null or else react throws
        if (!value) {
            return null;
        }
        // If library has not loaded yet, then just render the raw model string, better than empty
        if (!iOSDeviceList) {
            return value;
        }
        var deviceName = deviceNameMapper(value, iOSDeviceList);
        return (<span data-test-id="loaded-device-name">
        {children ? children(deviceName) : deviceName}
      </span>);
    };
    return DeviceName;
}(React.Component));
exports.default = DeviceName;
//# sourceMappingURL=deviceName.jsx.map