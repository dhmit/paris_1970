import { MapControl, withLeaflet } from 'react-leaflet';
import L from 'leaflet';
import './legend.scss';

class Legend extends MapControl {
    createLeafletElement(_props) {}

    componentDidMount() {
        // get color depending on the bucket that corresponds with the number of photos
        const getColor = (d) => {
            if (d === 1) {
                return '#E85285';
            }
            if (d === 2) {
                return '#C9458B';
            }
            if (d === 3) {
                return '#A93790';
            }
            if (d === 4) {
                return '#8A2995';
            }
            return '#6A1B9A';
        };

        const legend = L.control({ position: 'topright' });

        legend.onAdd = () => {
            const div = L.DomUtil.create('div', 'heat-map-info heat-map-legend');
            const grades = this.props.buckets;
            const labels = [];
            let d = 0;

            for (let i = 0; i < 9; i += 2) {
                d += 1;

                labels.push(
                    '<i style="background:' + getColor(d) + '"></i> '
                    + grades[i] + '&ndash;' + grades[i + 1],
                );
            }

            div.innerHTML = '<h6>Photo Density</h6>';
            div.innerHTML += '(photos/square)<br/>';
            div.innerHTML += labels.join('<br/>');
            return div;
        };

        const { map } = this.props.leaflet;
        legend.addTo(map);
    }
}

export default withLeaflet(Legend);

