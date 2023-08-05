Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var locale_1 = require("app/locale");
var EventPackageData = /** @class */ (function (_super) {
    tslib_1.__extends(EventPackageData, _super);
    function EventPackageData() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventPackageData.prototype.shouldComponentUpdate = function (nextProps) {
        return this.props.event.id !== nextProps.event.id;
    };
    EventPackageData.prototype.render = function () {
        var event = this.props.event;
        var longKeys, title;
        var packages = Object.entries(event.packages || {}).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                value: value,
                subject: key,
                meta: metaProxy_1.getMeta(event.packages, key),
            });
        });
        switch (event.platform) {
            case 'csharp':
                longKeys = true;
                title = locale_1.t('Assemblies');
                break;
            default:
                longKeys = false;
                title = locale_1.t('Packages');
        }
        return (<eventDataSection_1.default type="packages" title={title}>
        <clippedBox_1.default>
          <errorBoundary_1.default mini>
            <keyValueList_1.default data={packages} longKeys={longKeys}/>
          </errorBoundary_1.default>
        </clippedBox_1.default>
      </eventDataSection_1.default>);
    };
    return EventPackageData;
}(react_1.Component));
exports.default = EventPackageData;
//# sourceMappingURL=packageData.jsx.map