Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var contextData_1 = tslib_1.__importDefault(require("app/components/contextData"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var locale_1 = require("app/locale");
var DeviceInterface = function (_a) {
    var event = _a.event;
    var data = event.device || {};
    var extras = Object.entries(data.data || {}).map(function (_a) {
        var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
        return (<tr key={key}>
        <td className="key">{key}</td>
        <td className="value">
          <contextData_1.default data={value}/>
        </td>
      </tr>);
    });
    return (<eventDataSection_1.default type="device" title={locale_1.t('Device')} wrapTitle>
      <table className="table key-value">
        <tbody>
          {data.name && (<tr>
              <td className="key">Name</td>
              <td className="value">
                <pre>{data.name}</pre>
              </td>
            </tr>)}
          {data.version && (<tr>
              <td className="key">Version</td>
              <td className="value">
                <pre>{data.version}</pre>
              </td>
            </tr>)}
          {data.build && (<tr>
              <td className="key">Build</td>
              <td className="value">
                <pre>{data.build}</pre>
              </td>
            </tr>)}
          {extras}
        </tbody>
      </table>
    </eventDataSection_1.default>);
};
exports.default = DeviceInterface;
//# sourceMappingURL=device.jsx.map