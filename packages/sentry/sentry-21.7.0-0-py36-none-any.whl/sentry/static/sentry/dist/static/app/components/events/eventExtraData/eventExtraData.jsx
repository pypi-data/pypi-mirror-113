Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var locale_1 = require("app/locale");
var eventDataContent_1 = tslib_1.__importDefault(require("./eventDataContent"));
var EventExtraData = react_1.memo(function (_a) {
    var event = _a.event;
    var _b = tslib_1.__read(react_1.useState(false), 2), raw = _b[0], setRaw = _b[1];
    return (<eventDataSection_1.default type="extra" title={locale_1.t('Additional Data')} toggleRaw={function () { return setRaw(!raw); }} raw={raw}>
        <eventDataContent_1.default raw={raw} data={event.context}/>
      </eventDataSection_1.default>);
}, function (prevProps, nextProps) { return prevProps.event.id !== nextProps.event.id; });
exports.default = EventExtraData;
//# sourceMappingURL=eventExtraData.jsx.map