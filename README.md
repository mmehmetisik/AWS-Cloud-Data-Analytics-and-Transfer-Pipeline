# AWS Cloud Data Analytics and Transfer Pipeline

This repository showcases an end-to-end data analytics and transfer pipeline developed for a continuous operating facility using AWS Cloud infrastructure. The project features automated data processing from generation to visualization in custom dashboards tailored for various managerial levels.

## Features

- Automated data capture and processing using AWS Lambda and RDS.
- Real-time data transfer and storage with AWS S3 Buckets.
- Customized dashboards for data visualization, adapted for different user roles.

## Usage

To replicate or utilize this pipeline:

1. Ensure you have the necessary AWS services enabled (Lambda, RDS, S3, etc.).
2. Configure the AWS services according to the architecture provided in the `images` folder.
3. Use the provided scripts and AWS IAM roles to manage data flow and permissions.

For visualizing data:

1. Access the custom dashboards through the URLs provided in the `dashboards` folder.
2. Follow the instructions in `dashboard_setup.md` to tailor the dashboards to specific managerial roles.

## Contributing

To contribute to this project:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a new Pull Request.

## Acknowledgments

Special thanks to the team members and contributors who have made this project possible:
- Nurşah Söğüt
- Damla Peker
- Sinan (for guidance and contributions to the project)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
