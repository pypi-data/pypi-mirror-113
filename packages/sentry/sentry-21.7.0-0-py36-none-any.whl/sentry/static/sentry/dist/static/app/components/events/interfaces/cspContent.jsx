Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
function CSPContent(_a) {
    var data = _a.data;
    return (<div>
      <h4>
        <span>{data.effective_directive}</span>
      </h4>
      <keyValueList_1.default data={Object.entries(data).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                subject: key,
                value: value,
                meta: metaProxy_1.getMeta(data, key),
            });
        })} isContextData/>
    </div>);
}
exports.default = CSPContent;
//# sourceMappingURL=cspContent.jsx.map